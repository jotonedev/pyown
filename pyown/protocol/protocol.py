import asyncio
import logging
from asyncio import BaseTransport, Future, Protocol, Queue, Transport
from threading import Lock

from ..exceptions import ParseError
from ..messages import BaseMessage, parse_message

__all__ = [
    "OWNProtocol",
]

log = logging.getLogger("pyown.protocol")


class OWNProtocol(Protocol):
    """Asyncio protocol for the OpenWebNet TCP connection.

    Handles the connection lifecycle with the gateway, parses incoming data into
    messages, and sends outgoing messages.
    """

    _transport: Transport
    _lock: Lock

    def __init__(
        self,
        on_connection_start: Future[Transport],
        on_connection_end: Future[Exception | None],
    ):
        """Creates the TCP connection with the gateway, parses the incoming data, and sends the outgoing messages.

        Args:
            on_connection_start (Future): The future to set when the connection starts.
            on_connection_end (Future): The future to set when the connection ends.
        """
        self._on_connection_start: Future[Transport] = on_connection_start
        self._on_connection_end: Future[Exception | None] = on_connection_end

        # The queue was chosen because it supports both synchronous and asynchronous functions
        self._messages_queue: Queue[BaseMessage] = asyncio.Queue()

        self._lock = Lock()

    def connection_made(self, transport: BaseTransport):
        """Called by the transport class when the socket is connected to the server."""
        log.info("Connection made")
        if not isinstance(transport, Transport):
            raise TypeError("Expected a full-duplex Transport for the connection")
        self._transport = transport
        self._on_connection_start.set_result(transport)

    def connection_lost(self, exc: Exception | None):
        """Called by the transport class when the connection is lost or closed."""
        if exc is not None:
            log.info(f"Connection lost with exception: {exc}")
        else:
            log.info("Connection lost")
        if exc is None:
            self._on_connection_end.set_result(None)
        else:
            self._on_connection_end.set_exception(exc)

    def data_received(self, data: bytes):
        """Called by the transport class when a packet with data is received.

        The data argument is a bytes object containing the incoming data.
        It tries to parse the data, and if a valid message is found, it is added to the message queue.

        Args:
            data (bytes): The incoming data
        """
        # In OpenWebNet, the message is always written with ascii characters
        try:
            text = data.decode("ascii").strip()
        except UnicodeDecodeError as e:
            log.warning(f"Received data not ascii: {data.hex()}")
            raise e

        # Sometimes multiple messages can be sent in the same packet
        try:
            messages = [parse_message(msg + "##") for msg in text.split("##") if msg]
        except ParseError as e:
            log.warning(f"Received invalid message: {e}")
            raise e

        # If there are no messages, return
        if not messages:
            return

        log.debug(f"Received messages: {messages}")

        # Call the on_message_received future
        for msg in messages:
            self._messages_queue.put_nowait(msg)

    def pause_writing(self):
        """Called when the transport's buffer goes over the high-water mark."""
        self._lock.acquire()
        log.debug("Paused writing")

    def resume_writing(self):
        """Called when the transport buffer drains below the low-water mark."""
        self._lock.release()
        log.debug("Resumed writing")

    async def send_message(self, msg: BaseMessage, delay: float = 0.1):
        """Sends a message to the server.

        Args:
            msg (BaseMessage): The message to send
            delay (float): The delay to wait before sending the message.
                If the messages are sent too fast, certain servers will respond with invalid messages.
        """
        data = msg.bytes

        # block multiple messages from being sent at the same time
        while self._lock.locked():
            await asyncio.sleep(delay)

        self._transport.write(data)
        log.debug(f"Sent message: {msg}")

    async def receive_messages(self) -> BaseMessage:
        """Awaits a message from the server and returns it.

        Returns:
            BaseMessage: The message from the server, it will be a subclass of BaseMessage
        """
        messages = await self._messages_queue.get()
        return messages
