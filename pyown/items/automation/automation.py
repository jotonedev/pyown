from asyncio import Task
from enum import StrEnum, Enum, auto
from typing import Callable, Self, Coroutine, AsyncIterator

from ..base import BaseItem, CoroutineCallback
from ...exceptions import InvalidMessage
from ...messages import BaseMessage, NormalMessage
from ...tags import Who, What
from ...tags.where import Where

__all__ = [
    "Automation",
    "WhatAutomation",
    "AutomationEvents",
]


class AutomationEvents(Enum):
    """
    This enum is used internally to register the callbacks to the correct event.

    Attributes:
        STOP: The event for when the automation stops.
        UP: The event for when the automation goes up.
        DOWN: The event for when the automation goes down.
        ALL: The event for all events.
    """
    STOP = auto()
    UP = auto()
    DOWN = auto()
    ALL = auto()  # For all events


class WhatAutomation(What, StrEnum):
    """
    This enum contains the possible commands and states for an automation.

    Attributes:
        STOP: The command to stop the automation.
        UP: The command to go up.
        DOWN: The command to go down.
    """
    STOP = "0"
    UP = "1"
    DOWN = "2"


class Automation(BaseItem):
    """
    Automation items are usually used to control blinds, shutters, etc...
    """
    _who = Who.AUTOMATION

    _event_callbacks: dict[AutomationEvents, list[CoroutineCallback]] = {}

    async def stop(self):
        """Sends a stop command to the automation."""
        await self.send_normal_message(WhatAutomation.STOP)

    async def up(self):
        """Sends an up command to the automation."""
        await self.send_normal_message(WhatAutomation.UP)

    async def down(self):
        """Sends a down command to the automation."""
        await self.send_normal_message(WhatAutomation.DOWN)

    async def get_status(self) -> AsyncIterator[tuple[Where, WhatAutomation]]:
        """
        Requests the status of the automation.

        Raises:
            AttributeError: If the automation is not a light point.

        Returns:
            WhatAutomation: The status of the automation.
        """
        async for message in self.send_status_request():
            yield message.where, WhatAutomation(str(message.what))

    @classmethod
    def on_status_change(cls, callback: Callable[[Self, WhatAutomation], Coroutine[None, None, None]]):
        """
        Registers a callback to be called when the status of the automation changes.

        If the shutter is already down and a command is sent to go down, the gateway will sometimes return
        the stop event and before the down event. So, make sure to handle this case in your code.

        Args:
            callback (Callable[[Self, WhatAutomation], Coroutine[None, None, None]]): The callback to call.
                It will receive as arguments the item and the status.
        """
        cls._event_callbacks.setdefault(AutomationEvents.ALL, []).append(callback)

    @classmethod
    async def call_callbacks(cls, item: Self, message: BaseMessage) -> list[Task]:
        tasks: list[Task] = []

        if isinstance(message, NormalMessage):
            tasks += cls._create_tasks(
                cls._event_callbacks.get(AutomationEvents.ALL, []),
                item,
                WhatAutomation(str(message.what))
            )
        else:
            raise InvalidMessage(str(message))

        return tasks
