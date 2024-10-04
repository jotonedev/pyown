import asyncio
import logging
from asyncio import Protocol, Transport, Future, Queue

from ..exceptions import ParseError
from ..messages import BaseMessage, parse_message

__all__ = [
    "OWNProtocol",
]

log = logging.getLogger("pyown.protocol")


class OWNProtocol(Protocol):
    _transport: Transport

    def __init__(
            self,
            on_connection_start: Future[Transport],
            on_connection_end: Future[Exception | None],
    ):
        """
        Initialize the protocol.

        Args:
            on_connection_start (Future): The future to set when the connection starts.
            on_connection_end (Future): The future to set when the connection ends.
        """
        self._on_connection_start: Future[Transport] = on_connection_start
        self._on_connection_end: Future[Exception | None] = on_connection_end

        # The queue was chosen because it supports both synchronous and asynchronous functions
        # It contains list of messages to ensure that when multiple messages are sent in a packet, they are all consumed
        # This happens when the server sends, for example, a dimension response followed by an ACK even if the response
        # is itself a confirmation that the request was successful.
        self._messages_queue: Queue[list[BaseMessage]] = asyncio.Queue()

    def connection_made(self, transport: Transport):
        """
        Called when the socket is connected.
        """
        log.info(f"Connection made")
        self._transport = transport
        self._on_connection_start.set_result(transport)

    def connection_lost(self, exc: Exception | None):
        """
        Called when the connection is lost or closed.
        """
        log.info(f"Connection lost {f' with exception: {exc}' if exc is not None else ''}")
        if exc is None:
            self._on_connection_end.set_result(None)
        else:
            self._on_connection_end.set_exception(exc)

    def data_received(self, data: bytes):
        """
        Called when some data is received.

        The data argument is a bytes object containing the incoming data.
        It tries to parse the data and call the on_message_received for each message received.

        Args:
            data (bytes): The incoming data

        Returns:
            None
        """
        # In OpenWebNet, the message is always written with ascii characters
        try:
            data = data.decode("ascii").strip()
        except UnicodeDecodeError as e:
            log.warning(f"Received data is not ascii: {data.hex()}")
            raise e

        # Sometimes multiple messages can be sent in the same packet
        try:
            messages = [parse_message(msg + "##") for msg in data.split("##") if msg]
        except ParseError as e:
            log.warning(f"Received invalid message: {e.tags}")
            raise e

        # If there are no messages, return
        if not messages:
            return

        log.debug(f"Received messages: {messages}")

        # Call the on_message_received future
        self._messages_queue.put_nowait(messages)

    def send_message(self, msg: BaseMessage):
        """
        Send a message to the server.

        Args:
            msg (BaseMessage): The message to send
        """
        data = msg.bytes
        self._transport.write(data)
        log.debug(f"Sent message: {data}")

    async def receive_messages(self) -> list[BaseMessage]:
        """
        Receive a list of messages from the server.

        Returns:
            list[BaseMessage]: a list of messages that were sent in the same packet.
        """
        messages = await self._messages_queue.get()
        return messages
