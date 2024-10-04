import asyncio
import logging
from asyncio import AbstractEventLoop, Transport, Future
from typing import Optional

from ..auth import AuthAlgorithm
from ..auth.hmac import *
from ..auth.open import *
from ..exceptions import *
from ..messages import BaseMessage, MessageType, GenericMessage, NACK, ACK
from ..protocol import OWNProtocol, SessionType

__all__ = [
    "BaseClient",
]

log = logging.getLogger("pyown.client")


class BaseClient:
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

        Args:
            host (str): The host to connect to (ip address)
            port (int): The port to connect to
            password (str): The password to authenticate with
            session_type (SessionType): The session type to use
        """
        self._host = host
        self._port = port
        self._password = password
        self._session_type = session_type

        self._transport: Optional[Transport] = None
        self._protocol: Optional[OWNProtocol] = None

        self._loop = loop or asyncio.get_event_loop()

        self._on_connection_start: Future[Transport] = self._loop.create_future()
        self._on_connection_end: Future[Exception | None] = self._loop.create_future()

    async def start(self) -> None:
        """
        Start the client

        Raises:
            TimeoutError: if the server does not respond
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
            messages = await self._protocol.receive_messages()

        if messages[0].type != MessageType.ACK:
            raise InvalidSession("Expected ACK message")

        log.debug("Starting handshake")

        # Send the session type
        resp = await self.send_message_with_response(self._session_type.to_message())

        # Authentication
        # if the next message is an ACK, the server does not require authentication
        # if it's a message with only a number, the server requires the open authentication algorithm
        # if it's a ∗98∗## open command, the server requires the hmac authentication algorithm
        if resp[0].type == MessageType.ACK:
            log.info("No authentication required")
            pass
        elif len(resp[0].tags) == 1:
            log.info("Using open authentication")
            await self._authenticate_open(nonce=resp[0].tags[0])
        elif resp[0].tags[0] == "98":
            log.info("Using hmac authentication")
            tag = resp[0].tags[1]
            await self._authenticate_hmac(
                hash_algorithm=tag,
            )

        else:
            raise InvalidSession("Invalid authentication response")

        log.info("Client ready")

    async def _authenticate_open(self, nonce: str) -> None:
        """
        Authenticate the client using the open authentication algorithm

        Args:
            nonce (str): The nonce sent by the server
        """
        enc = own_calc_pass(self._password, nonce)

        resp = await self.send_message_with_response(GenericMessage(["#" + enc]))

        if resp[0].type != MessageType.ACK:
            raise InvalidAuthentication("Invalid password")

    async def _authenticate_hmac(self, hash_algorithm: AuthAlgorithm | str) -> None:
        """
        Authenticate the client using the hmac authentication algorithm

        Args:
            hash_algorithm (AuthAlgorithm | str): The hash algorithm to use
        """
        # TODO: Check with a real device if the handshake is implemented correctly
        if isinstance(hash_algorithm, str):
            try:
                hash_algorithm = AuthAlgorithm.from_string(hash_algorithm)
            except ValueError:
                # Close the connection
                await self.send_message(NACK())
                raise InvalidAuthentication("Invalid hash algorithm")

        # Send an ACK to accept the algorithm and wait for the server key
        resp = await self.send_message_with_response(ACK())
        server_key = resp[0].tags[0]

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
        resp = await self.send_message_with_response(
            GenericMessage([hex_to_digits(client_key), hex_to_digits(client_auth.hex())])
        )

        resp = resp[0]

        if resp.type == MessageType.NACK:
            raise InvalidAuthentication("Invalid password")

        # Check the server authentication string with the one generated
        if not compare_hmac(
                server_auth,
                bytes.fromhex(hex_to_digits(resp.tags[0]))
        ):
            raise InvalidAuthentication("Invalid password")
        else:
            await self.send_message(ACK())

    async def send_message(self, message: BaseMessage) -> None:
        """
        Send a message to the server

        Args:
            message (BaseMessage): send to the server a subclass of BaseMessage
        """
        self._protocol.send_message(message)

    async def send_message_with_response(
            self,
            message: BaseMessage,
            timeout: int = 5
    ) -> list[BaseMessage]:
        """
        Send a message and return the response.
        Valid only when the client is in a command session, otherwise raise an exception

        Args:
            message (BaseMessage): send to the server a subclass of BaseMessage
            timeout (int): the number of seconds to wait before raising TimeoutError

        Returns:
            BaseMessage: the response from the server

        Raises:
            InvalidSession: if the client is not in a command session
            TimeoutError: if the server does not return the excepted number of messages in the defined period in seconds
        """
        if self._session_type == SessionType.EventSession:
            raise InvalidSession

        # Send message
        self._protocol.send_message(message)

        # Wait for the response
        async with asyncio.timeout(timeout):
            messages = await self._protocol.receive_messages()

        return messages

    async def close(self) -> None:
        """
        Close the client
        """
        self._transport.close()
