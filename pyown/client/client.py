import logging
from asyncio import AbstractEventLoop
from typing import Optional

from ..events import EventBus, bootstrap, get_item_type, get_parser
from ..exceptions import InvalidMessage, InvalidSession, InvalidTag, ParseError
from ..items.base import BaseItem
from ..messages import MessageType
from ..tags import Where, Who
from .base import BaseClient
from .session import SessionType

__all__ = [
    "Client",
]

log = logging.getLogger("pyown.client")


class Client(BaseClient):
    """High-level OpenWebNet client.

    Exposes a typed `events` bus. Subscribe to event dataclasses to react to
    bus traffic when the client is run as an EventSession:

    ```python
    client = Client(host, port, password, SessionType.EventSession)
    client.events.subscribe(LightStatusEvent, on_light_change)
    await client.start()
    await client.loop()
    ```
    """

    _items: dict[tuple[Who, Where], BaseItem]

    def __init__(
        self,
        host: str,
        port: int,
        password: str,
        session_type: SessionType = SessionType.CommandSession,
        *,
        loop: Optional[AbstractEventLoop] = None,
    ):
        """Initialise the client.

        Args:
            host: The host to connect to (IP address).
            port: The port to connect to.
            password: The password to authenticate with.
            session_type: The session type to use. Default is CommandSession.
            loop: The event loop to use.
        """
        super().__init__(host, port, password, session_type, loop=loop)

        self._items = {}
        bootstrap()
        self.events: EventBus = EventBus()

    def get_item(self, who: Who, where: Where, *, client: BaseClient) -> BaseItem:
        """Instantiate an item (or return the cached instance) for a given WHO/WHERE.

        Args:
            who: The type of the item.
            where: The location of the item.
            client: The client to assign to the item if it's not already defined.

        Raises:
            KeyError: if the item WHO is not supported.
        """
        if (who, where) in self._items:
            return self._items[(who, where)]
        factory = get_item_type(who)
        if factory is None:
            raise KeyError(f"Item factory not found: {who}, {where}")
        item = self._items[(who, where)] = factory(client, where)
        return item

    async def loop(self, *, client: BaseClient | None = None):
        """Run the client event loop.

        Reads messages from the gateway, instantiates the matching item, runs
        the registered parser to produce typed events, and dispatches them on
        `self.events`.

        Args:
            client: The client to use to instantiate items for callbacks. Default
                is self. Useful when items should have a command client so user
                handlers can send commands.

        Raises:
            InvalidSession: if called on a command session or if the client is
                not connected.
        """
        if self.is_cmd_session():
            raise InvalidSession("Cannot run loop on a command session")

        if self._transport is None:
            raise InvalidSession("Client is not connected")

        if client is None:
            client = self

        while not self._transport.is_closing():
            try:
                message = await self.read_message(timeout=None)
            except (ParseError, InvalidMessage, InvalidTag) as e:
                log.warning("Error reading message: %s", e)
                continue

            if message.type == MessageType.ACK or message.type == MessageType.NACK:
                continue
            elif message.type == MessageType.GENERIC:
                log.warning("Received an unknown message: %s", message)
                continue

            who, where = message.who, message.where

            if who is None or where is None:
                log.warning("Received a message without who or where: %s", message)
                continue

            try:
                item = self.get_item(who, where, client=client)
            except KeyError:
                log.info("Item type not supported, WHO=%s WHERE=%s", who, where)
                continue

            parser_fn = get_parser(who)
            if parser_fn is None:
                log.info("No parser registered for WHO=%s", who)
                continue

            try:
                events = list(parser_fn(item, message))
            except (InvalidMessage, InvalidTag) as e:
                log.warning("Parser rejected message %s: %s", message, e)
                continue
            except Exception as e:
                log.error("Parser raised: %s", e, exc_info=e)
                continue

            for event in events:
                self._loop.create_task(self.events.dispatch(event))
