import asyncio
import logging
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop, Transport, Future
from typing import Optional, Any

from .session import SessionType
from ..auth import AuthAlgorithm
from ..auth.hmac import server_hmac, client_hmac, hex_to_digits, compare_hmac, create_key
from ..auth.open import own_calc_pass
from ..exceptions import InvalidAuthentication, InvalidSession
from ..messages import BaseMessage, MessageType, GenericMessage, NACK, ACK
from ..protocol import OWNProtocol

__all__ = [
    "BaseClient",
]

log = logging.getLogger("pyown.client")


class BaseClient(ABC):
    def __init__(
            self,
            host: str,
            port: int,
            password: str,
            session_type: SessionType = SessionType.CommandSession,
            *,
            loop: Optional[AbstractEventLoop] = None
    ):
        """
        BaseClient constructor
        This class should not be instantiated directly, use the Client class instead

        Args:
            host (str): The host to connect to (ip address)
            port (int): The port to connect to
            password (str): The password to authenticate with
            session_type (SessionType): The session type to use
            loop (Optional[AbstractEventLoop]): The event loop to use
        """
        self._host = host
        self._port = port
        self._password = password
        self._session_type = session_type

        self._transport: Optional[Transport] = None
        self._protocol: Optional[OWNProtocol] = None

        self._loop = loop or asyncio.get_event_loop()
        self._loop.set_exception_handler(self._exception_handler)

        self._on_connection_start: Future[Transport] = self._loop.create_future()
        self._on_connection_end: Future[Exception | None] = self._loop.create_future()

    def is_cmd_session(self) -> bool:
        """
        Checks if the session is a command session

        Returns:
            bool: True if the session is a command session, False otherwise
        """
        return self._session_type == SessionType.CommandSession or self._session_type == SessionType.OldCommandSession

    async def start(self) -> None:
        """
        Creates a connection with the gateway and does the initial handshake

        Raises:
            TimeoutError: if the server does not respond
            InvalidSession: if the server requires an unknown authentication algorithm
        """
        self._transport, self._protocol = await self._loop.create_connection(
            lambda: OWNProtocol(
                on_connection_start=self._on_connection_start,
                on_connection_end=self._on_connection_end,
            ),
            self._host,
            self._port
        )

        # Wait for the connection to start
        await self._on_connection_start

        log.debug("Connection started")

        # Handshake
        # The first packet is from the server, and it's an ACK packet
        # The second packet is from the client and set the session type
        # Wait for the first packet
        async with asyncio.timeout(5):
            message = await self.read_message()

        if message.type != MessageType.ACK:
            raise InvalidAuthentication("Expected ACK message")

        log.debug("Starting handshake")

        # Send the session type
        await self.send_message(self._session_type.to_message(), force=True)
        resp = await self.read_message()

        # Authentication
        # if the next message is an ACK, the server does not require authentication
        # if it's a message with only a number, the server requires the open authentication algorithm
        # if it's a ∗98∗## open command, the server requires the hmac authentication algorithm
        if resp.type == MessageType.ACK:
            log.info("No authentication required")
        elif len(resp.tags) == 1:
            log.info("Using open authentication")
            await self._authenticate_open(nonce=resp.tags[0])
        elif resp.tags[0] == "98":
            log.info("Using hmac authentication")
            tag = resp.tags[1]
            await self._authenticate_hmac(
                hash_algorithm=tag,
            )
        else:
            raise InvalidAuthentication("Invalid authentication response")

        log.info("Client ready")

    async def _authenticate_open(self, nonce: str) -> None:
        """
        Authenticates the client using the open authentication algorithm

        Args:
            nonce (str): The nonce sent by the server
        """
        enc = own_calc_pass(self._password, nonce)

        await self.send_message(GenericMessage(["#" + enc]), force=True)
        resp = await self.read_message()

        if resp.type != MessageType.ACK:
            raise InvalidAuthentication("Invalid password")

    async def _authenticate_hmac(self, hash_algorithm: AuthAlgorithm | str) -> None:
        """
        Authenticates the client using the hmac authentication algorithm

        Args:
            hash_algorithm (AuthAlgorithm | str): The hash algorithm to use
        """
        # TODO: Check with a real device if the handshake is implemented correctly
        if isinstance(hash_algorithm, str):
            try:
                hash_algorithm = AuthAlgorithm.from_string(hash_algorithm)
            except ValueError:
                # Close the connection
                await self.send_message(NACK(), force=True)
                raise InvalidAuthentication("Invalid hash algorithm")

        # Send an ACK to accept the algorithm and wait for the server key
        await self.send_message(ACK(), force=True)
        resp = await self.read_message()
        server_key = resp.tags[0]

        # Generate the client key
        client_key = create_key(hash_algorithm)

        # Generate the two authentication strings
        client_auth = client_hmac(
            server_key=server_key,
            client_key=client_key,
            password=self._password,
            hash_algorithm=hash_algorithm
        )
        server_auth = server_hmac(
            server_key=server_key,
            client_key=client_key,
            password=self._password,
            hash_algorithm=hash_algorithm
        )

        # Send the client authentication string
        await self.send_message(
            GenericMessage([hex_to_digits(client_key), hex_to_digits(client_auth.hex())]),
            force=True
        )
        resp = await self.read_message()

        if resp.type == MessageType.NACK:
            raise InvalidAuthentication("Invalid password")

        # Check the server authentication string with the one generated
        if not compare_hmac(
                server_auth,
                bytes.fromhex(hex_to_digits(resp.tags[0]))
        ):
            raise InvalidAuthentication("Invalid password")
        else:
            await self.send_message(ACK(), force=True)

    async def send_message(self, message: BaseMessage, *, force: bool = False) -> None:
        """
        Sends a message to the server

        Args:
            message (BaseMessage): send to the server a subclass of BaseMessage
            force (bool): if True, the message will be sent even if the client is set as an event session

        Raises:
            InvalidSession: if the client is set as an event session or if the client is not started
        """
        if not self.is_cmd_session() and not force:
            raise InvalidSession("Cannot send messages in an event session")
        if self._protocol is None:
            raise InvalidSession("Client not started")

        await self._protocol.send_message(message)

    async def read_message(self, timeout: int | None = 5) -> BaseMessage:
        """
        Awaits a message from the server and returns it.

        Returns:
            BaseMessage: the message from the server, it will be a subclass of BaseMessage.

        Raises:
            TimeoutError: if the server does not respond in the given time.
            InvalidSession: if the client is not started.
        """
        if self._protocol is None:
            raise InvalidSession("Client not started")

        async with asyncio.timeout(timeout):
            message = await self._protocol.receive_messages()

        return message

    async def close(self) -> None:
        """
        Close the client
        """
        if self._transport is not None:
            self._transport.close()

        self._protocol = None
        self._transport = None

    @abstractmethod
    async def loop(self):
        """
        Runs the client loop.
        This is a loop that runs the entire event system for the client, it will read messages from the gateway and
        dispatch them to the correct callbacks.
        """
        raise NotImplementedError

    @staticmethod
    def _exception_handler(_: AbstractEventLoop, context: dict[str, Any]):
        exception = context.get("exception")
        message = context.get("message")

        if exception is not None:
            log.error(f"Exception occurred: {message} ({exception})")
        else:
            return

        if (task := context.get("task")) is not None:
            task.print_stack()
        elif (protocol := context.get("protocol")) is not None:
            log.error(f"Protocol error: {protocol}")
        elif (transport := context.get("transport")) is not None:
            log.error(f"Transport error: {transport}")
