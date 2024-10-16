import asyncio
import logging
from asyncio import AbstractEventLoop, Task
from typing import Optional

from .base import BaseClient
from ..exceptions import InvalidSession, ParseError, InvalidMessage, InvalidTag
from ..items.base import BaseItem
from ..items.utils import ITEM_TYPES
from ..messages import MessageType
from ..protocol import SessionType
from ..tags import Who, Where

__all__ = [
    "Client",
]

log = logging.getLogger("pyown.client")


class Client(BaseClient):
    _items: dict[tuple[Who, Where], BaseItem]

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
        Create a new client.

        Args:
            host (str): The host to connect to (ip address)
            port (int): The port to connect to
            password (str): The password to authenticate with
            session_type (SessionType): The session type to use.
            Default is CommandSession
            loop (Optional[AbstractEventLoop]): The event loop to use
        """
        super().__init__(host, port, password, session_type, loop=loop)

        self._items = {}

    def get_item(self, who: Who, where: Where, *, client: BaseClient) -> BaseItem:
        """
        Get an item from the client.

        Args:
            who: The type of the item.
            where: The location of the item.
            client: The client to use to declare the items if they are already declared.

        Returns:
            The item.

        Raises:
            KeyError: if the item is not found.
        """
        if (who, where) in self._items:
            return self._items[(who, where)]
        else:
            factory = ITEM_TYPES.get(who)
            if factory is not None:
                item = self._items[(who, where)] = factory(self, where)
                return item
            else:
                raise KeyError(f"Item not found: {who}, {where}")

    async def loop(self, *, client: BaseClient | None = None):
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

        Args:
            client: The client to use to declare the items for the callbacks.
            Default is self.

        Returns:
            None

        Raises:
            InvalidSession: if called when the client is set as a command client and not as an event client or
            if the client is not connected
        """
        if self.is_cmd_session():
            raise InvalidSession("Cannot run loop on a command session")

        if self._transport is None:
            raise InvalidSession("Client is not connected")

        if client is None:
            client = self

        # loop until the connection is dropped or closed
        while not self._transport.is_closing():
            try:
                # by putting timeout as None, it will wait indefinitely for a message
                message = await self.read_message(timeout=None)
            except (ParseError, InvalidMessage, InvalidTag) as e:
                log.warning("Error reading message: %s", e)
                continue

            # ignore status messages
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
                # get item if already declared, otherwise instantiate it
                item = self.get_item(who, where, client=client)
            except KeyError:
                log.info(f"Item type not supported, WHO={who}, WHERE={where}")
                continue

            # because callbacks are defined inside items, we need to loop through all items to find the correct one
            for item_obj in BaseItem.__subclasses__():
                if message.who == item_obj.who:
                    try:
                        tasks = item_obj.call_callbacks(item, message)
                    except ValueError:
                        log.warning(f"Message not supported {message}")
                    else:
                        self._loop.create_task(self._check_task_result(tasks))
                        break
            else:
                log.warning(f"Item not found for message {message}")

    @staticmethod
    async def _check_task_result(tasks: list[Task]):
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, r in enumerate(results):
            if isinstance(r, Exception):
                log.error(f"Error in callback {r}")
                tasks[i].print_stack()
