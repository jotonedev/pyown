from abc import ABC, abstractmethod
from asyncio import Task
from enum import StrEnum, Enum, auto
from typing import Callable, Self, Coroutine, AsyncIterator

from ..base import BaseItem, CoroutineCallback
from ...messages import DimensionResponse, BaseMessage, NormalMessage
from ...tags import Who, What, Value, Where

__all__ = [
    "BaseLight",
    "WhatLight",
    "LightEvents",
]


class LightEvents(Enum):
    STATUS_CHANGE = auto()
    LUMINOSITY_CHANGE = auto()
    LIGHT_TEMPORIZATION = auto()
    HSV_CHANGE = auto()
    WHITE_TEMP_CHANGE = auto()


class WhatLight(What, StrEnum):
    OFF = "0"
    ON = "1"

    # Dimmer only
    ON_20_PERCENT = "2"
    ON_30_PERCENT = "3"
    ON_40_PERCENT = "4"
    ON_50_PERCENT = "5"
    ON_60_PERCENT = "6"
    ON_70_PERCENT = "7"
    ON_80_PERCENT = "8"
    ON_90_PERCENT = "9"
    ON_100_PERCENT = "10"

    ON_1_MIN = "11"
    ON_2_MIN = "12"
    ON_3_MIN = "13"
    ON_4_MIN = "14"
    ON_5_MIN = "15"
    ON_15_MIN = "16"
    ON_30_MIN = "17"
    ON_0_5_SEC = "18"

    BLINKING_0_5_SEC = "20"
    BLINKING_1_0_SEC = "21"
    BLINKING_1_5_SEC = "22"
    BLINKING_2_0_SEC = "23"
    BLINKING_2_5_SEC = "24"
    BLINKING_3_0_SEC = "25"
    BLINKING_3_5_SEC = "26"
    BLINKING_4_0_SEC = "27"
    BLINKING_4_5_SEC = "28"
    BLINKING_5_0_SEC = "29"

    # Dimmer only
    UP_1_PERCENT = "30"  # Support parameter to change the percentage
    DOWN_1_PERCENT = "31"  # Support parameter to change the percentage

    COMMAND_TRANSLATION = "1000"


class BaseLight(BaseItem, ABC):
    """Base class for all light items."""
    _who: Who = Who.LIGHTING

    _event_callbacks: dict[LightEvents, list[CoroutineCallback]] = {}

    async def turn_on(self):
        """Turns the light on."""
        await self.send_normal_message(WhatLight.ON)

    async def turn_off(self):
        """Turns the light off."""
        await self.send_normal_message(WhatLight.OFF)

    async def turn_on_1_min(self):
        """Turns the light on for 1 minute."""
        await self.send_normal_message(WhatLight.ON_1_MIN)

    async def turn_on_2_min(self):
        """Turns the light on for 2 minutes."""
        await self.send_normal_message(WhatLight.ON_2_MIN)

    async def turn_on_3_min(self):
        """Turns the light on for 3 minutes."""
        await self.send_normal_message(WhatLight.ON_3_MIN)

    async def turn_on_4_min(self):
        """Turns the light on for 4 minutes."""
        await self.send_normal_message(WhatLight.ON_4_MIN)

    async def turn_on_5_min(self):
        """Turns the light on for 5 minutes."""
        await self.send_normal_message(WhatLight.ON_5_MIN)

    async def turn_on_15_min(self):
        """Turns the light on for 15 minutes."""
        await self.send_normal_message(WhatLight.ON_15_MIN)

    async def turn_on_30_min(self):
        """Turns the light on for 30 minutes."""
        await self.send_normal_message(WhatLight.ON_30_MIN)

    async def turn_on_0_5_sec(self):
        """Turns the light on for 0.5 seconds."""
        await self.send_normal_message(WhatLight.ON_0_5_SEC)

    @abstractmethod
    async def get_status(self) -> AsyncIterator[tuple[Where, bool | int]]:
        """Gets the status of the light"""
        yield None  # type: ignore[misc]

    async def temporization_command(self, hour: int, minute: int, second: int):
        """
        Sends a temporization command

        It will turn the light immediately on and then off after the specified time passed.

        Args:
            hour: It indicates show many hours the actuator has to stay ON
            minute: It indicates show many minutes the actuator has to stay ON
            second: It indicates show many seconds the actuator has to stay ON
        """
        if hour >= 24 or minute >= 60 or second >= 60:
            raise ValueError("Invalid time")

        await self.send_dimension_writing("2", Value(hour), Value(minute), Value(second))

    async def temporization_request(self) -> AsyncIterator[tuple[Where, int, int, int]]:
        """
        Requests the gateway the current temporization settings of the actuator.

        Yields:
            A tuple with the hour, minute, and second of the temporization.
        """
        async for message in self.send_dimension_request("2"):
            hour = int(message.values[0].tag)  # type: ignore[arg-type]
            minute = int(message.values[1].tag)  # type: ignore[arg-type]
            second = int(message.values[2].tag)  # type: ignore[arg-type]
            yield message.where, hour, minute, second

    async def request_working_time_lamp(self) -> AsyncIterator[tuple[Where, int]]:
        """
        Requests the gateway for how long the light has been on.

        Yields:
            The time in hours the light has been on.
            The value is in the range [1-100000].
        """
        async for message in self.send_dimension_request("3"):
            yield message.where, int(message.values[0].tag)  # type: ignore[arg-type]

    @classmethod
    def on_status_change(cls, callback: Callable[[Self, bool], Coroutine[None, None, None]]):
        """
        Registers a callback function to be called when the light status changes.

        Args:
            callback: The callback function to call.
            It will receive as arguments the item and the status.
        """
        cls._event_callbacks.setdefault(LightEvents.STATUS_CHANGE, []).append(callback)

    @classmethod
    def on_temporization_change(cls, callback: Callable[[Self, int, int, int], Coroutine[None, None, None]]):
        """
        Registers a callback function to be called when the temporization changes.

        Args:
            callback: The callback function to call.
            It will receive as arguments the item, the hour, the minute, and the second.
        """
        cls._event_callbacks.setdefault(LightEvents.LIGHT_TEMPORIZATION, []).append(callback)

    @classmethod
    def call_callbacks(cls, item: BaseItem, message: BaseMessage) -> list[Task]:
        """
        Calls the registered callbacks for the event.

        Args:
            item: The item that triggered the event.
            message: The message that triggered the event.
        """
        tasks: list[Task] = []

        if isinstance(message, DimensionResponse):
            if message.dimension.tag == "1":
                tasks += cls._create_tasks(
                    cls._event_callbacks.get(LightEvents.LIGHT_TEMPORIZATION, []),
                    item,
                    int(message.values[0].tag),  # type: ignore[arg-type]
                    int(message.values[1].tag),  # type: ignore[arg-type]
                    int(message.values[2].tag)  # type: ignore[arg-type]
                )
            elif message.dimension.tag == "8":
                tasks += cls._create_tasks(
                    cls._event_callbacks.get(LightEvents.LUMINOSITY_CHANGE, []),
                    item,
                    int(message.values[0].tag),  # type: ignore[arg-type]
                    int(message.values[1].tag)  # type: ignore[arg-type]
                )
            elif message.dimension.tag == "12":
                tasks += cls._create_tasks(
                    cls._event_callbacks.get(LightEvents.HSV_CHANGE, []),
                    item,
                    int(message.values[0].tag),  # type: ignore[arg-type]
                    int(message.values[1].tag),  # type: ignore[arg-type]
                    int(message.values[2].tag)  # type: ignore[arg-type]
                )
            elif message.dimension.tag == "13":
                tasks += cls._create_tasks(
                    cls._event_callbacks.get(LightEvents.WHITE_TEMP_CHANGE, []),
                    item,
                    int(message.values[0].tag)  # type: ignore[arg-type]
                )
        elif isinstance(message, NormalMessage):
            tasks += cls._create_tasks(
                cls._event_callbacks.get(LightEvents.STATUS_CHANGE, []),
                item,
                message.what == WhatLight.ON
            )
        else:
            raise ValueError(f"Invalid message: {message}")

        return tasks
