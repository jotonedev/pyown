import asyncio
import logging
from asyncio import Protocol, Transport
from typing import TYPE_CHECKING, Callable, Awaitable, Type

from ..exceptions import ParseError
from ..messages import BaseMessage, parse_message

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from asyncio.futures import Future

__all__ = [
    "OWNProtocol",
]

log = logging.getLogger("pyown.protocol")


class OWNProtocol(Protocol):
    _transport: Transport

    def __init__(
            self,
            loop: AbstractEventLoop,
            on_session_start: Future | None = None,
            on_session_end: Future | None = None,
            on_message_received: Callable[[Type[BaseMessage]], Awaitable[None]] | None = None,
    ):
        """
        Initialize the protocol.

        Args:
            loop (AbstractEventLoop): The event loop
            on_session_start (Future, optional): The future to set when the session starts. Defaults to None.
            on_session_end (Future, optional): The future to set when the session ends. Defaults to None.
            on_message_received (Callable[[Type[BaseMessage]], Awaitable[None], optional):
            The async callback to call when a message is received. Defaults to None.

        Returns:
            None
        """
        self._loop = loop

        self._on_connection_start: Future | None = on_session_start
        self._on_connection_end: Future | None = on_session_end
        self._on_message_received: Callable[[Type[BaseMessage]], Awaitable[None]] | None = on_message_received

    def connection_made(self, transport: Transport):
        """
        Called when the socket is connected.
        """
        log.info(f"Connection made with {transport.get_extra_info('peername')}")
        self._transport = transport
        self._on_connection_start.set_result(True)

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
        except UnicodeDecodeError:
            log.warning(f"Received data is not ascii: {data.hex()}")
            self._transport.close()
            return

        # Sometimes multiple messages can be sent in the same packet
        try:
            messages = [parse_message(msg + "##") for msg in data.split("##") if msg]
        except ParseError:
            log.warning(f"Received invalid message: {data}")
            self._transport.close()
            return

        # If there are no messages, return
        if not messages:
            return

        # If the on_message_received is not set, return
        if self._on_message_received is None:
            return

        # Call the on_message_received for each message
        for msg in messages:
            log.debug(f"Received message: {msg}")

            asyncio.ensure_future(
                self._on_message_received(msg),
                loop=self._loop,
            )

    def connection_lost(self, exc: Exception | None):
        """
        Called when the connection is lost or closed.
        """
        log.info(
            f"Connection lost {f'with exception: {exc}' if exc is not None else ''} "
            f"to {self._transport.get_extra_info('peername')}"
        )
        self._on_connection_end.set_result(True)
