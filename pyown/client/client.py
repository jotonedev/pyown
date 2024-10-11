import logging
from typing import Callable, Awaitable

from .base import BaseClient
from ..exceptions import InvalidSession
from ..items.base import BaseItem, BaseEvents
from ..messages import MessageType, BaseMessage
from ..tags import Who, Where

__all__ = [
    "Client"
]

log = logging.getLogger("pyown.client")


class Client(BaseClient):
    _where_callback: dict[tuple[Who, Where], list[Callable[[BaseItem, BaseEvents], Awaitable[None]]]] = {}
    _who_callback: dict[Who, list[Callable[[BaseItem, BaseEvents], Awaitable[None]]]] = {}
    _default_callback: list[Callable[[BaseItem, BaseEvents], Awaitable[None]]] = []

    _items: dict[(Who, Where), BaseItem] = {}

    def add_callback(self, callback: Callable[[BaseItem, BaseEvents], Awaitable[None]]):
        """
        Add a callback to the client.
        It will be called every time a message is received.
        Must be used only when the client is set as an event client.

        Args:
            callback: the function to call when a message is received, it must accept two arguments: the item and the event

        Returns:
            None

        Raises:
            InvalidSession: if called when the client is set as a command client
        """
        if not self.is_cmd_session():
            self._default_callback.append(callback)
        else:
            raise InvalidSession("Cannot add callback to a command session")

    def add_who_callback(self, callback: Callable[[BaseItem, BaseEvents], Awaitable[None]], who: Who):
        """
        Add a callback to the client.
        It will be called every time a message with the specified who is received.
        Must be used only when the client is set as an event client.

        Args:
            callback: the function to call when a message is received, it must accept two arguments: the item and the event
            who: the who tag to listen to

        Returns:
            None

        Raises:
            InvalidSession: if called when the client is set as a command client
        """
        if not self.is_cmd_session():
            if who not in self._who_callback:
                self._who_callback[who] = []
            self._who_callback[who].append(callback)
        else:
            raise InvalidSession("Cannot add callback to a command session")

    def add_where_callback(self, callback: Callable[[BaseItem, BaseEvents], Awaitable[None]], who: Who, where: Where):
        """
        Add a callback to the client.
        It will be called every time a message with the specified who and where is received.
        Must be used only when the client is set as an event client.

        Args:
            callback: the function to call when a message is received, it must accept two arguments: the item and the event
            who: the who tag to listen to
            where: the where tag to listen to

        Returns:
            None

        Raises:
            InvalidSession: if called when the client is set as a command client
        """
        if not self.is_cmd_session():
            if (who, where) not in self._where_callback:
                self._where_callback[(who, where)] = []
            self._where_callback[(who, where)].append(callback)
        else:
            raise InvalidSession("Cannot add callback to a command session")

    def remove_callback(self, callback: Callable[[BaseItem, BaseEvents], Awaitable[None]]):
        """
        Remove a callback from the client.

        Args:
            callback: the function to remove

        Returns:
            None
        """
        # check if the callback is in every list and remove it
        for who, callbacks in self._who_callback.items():
            if callback in callbacks:
                callbacks.remove(callback)

        for (who, where), callbacks in self._where_callback.items():
            if callback in callbacks:
                callbacks.remove(callback)

        if callback in self._default_callback:
            self._default_callback.remove(callback)

    async def _call_callbacks(self, item: BaseItem, event: BaseMessage):
        """Call the callbacks for the specified item and event"""
        raise NotImplementedError

    async def _call_who_callbacks(self, item: BaseItem, event: BaseMessage):
        """Call the callbacks for the specified item and event"""
        raise NotImplementedError

    async def _call_where_callbacks(self, item: BaseItem, message: BaseMessage):
        """Call the callbacks for the specified item and event"""
        raise NotImplementedError

    def _item_factory(self, who: Who, where: Where) -> BaseItem:
        """Create a new item"""
        raise NotImplementedError

    async def loop(self):
        """
        Run the event loop until the client is closed
        This is not associated with the asyncio event loop.
        This will loop until the client is closed, and it will call the callbacks when a message is received.

        Typical usage:
        ```python
        client = Client(host, port, password, SessionType.EventSession)
        client.add_callback(lambda item, event: print(item, event))
        await client.connect()
        own_loop = asyncio.create_task(client.loop())

        # Do something else

        await client.close()
        ```

        Returns:
            None

        Raises:
            InvalidSession: if called when the client is set as a command client and not as an event client
        """
        if self.is_cmd_session():
            raise InvalidSession("Cannot run loop on a command session")

        while not self._transport.is_closing():
            message = await self.read_message(timeout=None)

            if message.type == MessageType.ACK or message.type == MessageType.NACK:
                continue
            elif message.type == MessageType.GENERIC:
                log.warning("Received an unknown message: %s", message)
                continue

            who, where = message.who, message.where

            if who is None or where is None:
                log.warning("Received a message without who or where: %s", message)
                continue

            if (who, where) in self._items:
                item = self._items[(who, where)]
            else:
                item = self._items[(who, where)] = self._item_factory(who, where)

            await self._call_callbacks(item, message)
            await self._call_who_callbacks(item, message)
            await self._call_where_callbacks(item, message)
