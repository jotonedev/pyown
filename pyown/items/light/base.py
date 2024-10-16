import asyncio
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from enum import StrEnum, Enum, auto
from typing import Callable, Self, Coroutine

from ..base import BaseItem
from ...exceptions import RequestError
from ...messages import DimensionResponse, BaseMessage, NormalMessage
from ...tags import Who, What, Value, Dimension

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


CoroutineCallback = Callable[..., Coroutine[None, None, None]]


class BaseLight(BaseItem, ABC):
    """Base class for all light items."""
    _who: Who = Who.LIGHTING

    _event_callbacks: dict[LightEvents, list[CoroutineCallback]] = {}

    async def turn_on(self):
        """Turn the light on."""
        await self.send_normal_message(WhatLight.ON)

    async def turn_off(self):
        """Turn the light off."""
        await self.send_normal_message(WhatLight.OFF)

    async def turn_on_1_min(self):
        """Turn the light on for 1 minute."""
        await self.send_normal_message(WhatLight.ON_1_MIN)

    async def turn_on_2_min(self):
        """Turn the light on for 2 minutes."""
        await self.send_normal_message(WhatLight.ON_2_MIN)

    async def turn_on_3_min(self):
        """Turn the light on for 3 minutes."""
        await self.send_normal_message(WhatLight.ON_3_MIN)

    async def turn_on_4_min(self):
        """Turn the light on for 4 minutes."""
        await self.send_normal_message(WhatLight.ON_4_MIN)

    async def turn_on_5_min(self):
        """Turn the light on for 5 minutes."""
        await self.send_normal_message(WhatLight.ON_5_MIN)

    async def turn_on_15_min(self):
        """Turn the light on for 15 minutes."""
        await self.send_normal_message(WhatLight.ON_15_MIN)

    async def turn_on_30_min(self):
        """Turn the light on for 30 minutes."""
        await self.send_normal_message(WhatLight.ON_30_MIN)

    async def turn_on_0_5_sec(self):
        """Turn the light on for 0.5 seconds."""
        await self.send_normal_message(WhatLight.ON_0_5_SEC)

    @abstractmethod
    async def get_status(self) -> bool | int:
        """Get the status of the light"""
        raise NotImplementedError

    async def temporization_command(self, hour: int, minute: int, second: int):
        """
        Send a temporization command

        It will turn the light immediately on and then off after the specified time passed.

        Args:
            hour: The number of hours to wait before turning off the light.
            minute: The number of minutes to wait before turning off the light.
            second: The number of seconds to wait before turning off the light.
        """
        if hour >= 24 or minute >= 60 or second >= 60:
            raise ValueError("Invalid time")

        await self.send_dimension_writing("2", Value(hour), Value(minute), Value(second))

    async def request_current_temporization(self):
        """
        Request the gateway the last temporization command sent.

        The response will be sent to the event session.
        """
        msg = self.create_dimension_request_message(Dimension("1"))
        await self._send_message(msg)

        resp = await self._read_message()
        self._check_ack(resp)

    async def request_working_time_lamp(self) -> int:
        """
        Request the gateway for how long the light has been on.

        Returns:
            The time in seconds the light has been on.

        Raises:
            RequestError: If the response is not what was expected.
        """

        msg = self.create_dimension_request_message(Dimension("8"))
        await asyncio.sleep(1)
        await self._send_message(msg)

        resp = await self._read_message()
        self._check_nack(resp)

        ack = await self._read_message()
        self._check_ack(ack)

        if not isinstance(resp, DimensionResponse):
            raise RequestError(f"Error sending message: {msg}, response: {resp}")

        if resp.values[0].tag is not None:
            return int(resp.values[0].tag)
        else:
            raise RequestError(f"Invalid response: {resp}")

    @classmethod
    def on_status_change(cls, callback: Callable[[Self, bool], Coroutine[None, None, None]]):
        """
        Register a callback function to be called when the light status changes.

        Args:
            callback: The callback function to call.
            It will receive as arguments the item and the status.
        """
        cls._event_callbacks.setdefault(LightEvents.STATUS_CHANGE, []).append(callback)

    @classmethod
    def on_temporization_change(cls, callback: Callable[[Self, int, int, int], Coroutine[None, None, None]]):
        """
        Register a callback function to be called when the temporization changes.

        Args:
            callback: The callback function to call.
            It will receive as arguments the item, the hour, the minute, and the second.
        """
        cls._event_callbacks.setdefault(LightEvents.LIGHT_TEMPORIZATION, []).append(callback)

    @classmethod
    def call_callbacks(cls, item: BaseItem, message: BaseMessage, *, loop: AbstractEventLoop | None = None) -> None:
        """
        Call the registered callbacks for the event.

        Args:
            item: The item that triggered the event.
            message: The message that triggered the event.
            loop: The event loop to use, default is asyncio.get_event_loop()
        """
        loop = loop or asyncio.get_event_loop()

        if isinstance(message, DimensionResponse):
            if message.dimension.tag == "1":
                for callback in cls._event_callbacks.get(LightEvents.LIGHT_TEMPORIZATION, []):
                    loop.create_task(
                        callback(
                            item,
                            int(message.values[0].tag),  # type: ignore[arg-type]
                            int(message.values[1].tag),  # type: ignore[arg-type]
                            int(message.values[2].tag)  # type: ignore[arg-type]
                        )
                    )
            elif message.dimension.tag == "8":
                for callback in cls._event_callbacks.get(LightEvents.LUMINOSITY_CHANGE, []):
                    loop.create_task(
                        callback(
                            item,
                            int(message.values[0].tag),  # type: ignore[arg-type]
                            int(message.values[1].tag)  # type: ignore[arg-type]
                        )
                    )
            elif message.dimension.tag == "12":
                for callback in cls._event_callbacks.get(LightEvents.HSV_CHANGE, []):
                    loop.create_task(
                        callback(
                            item,
                            int(message.values[0].tag),  # type: ignore[arg-type]
                            int(message.values[1].tag),  # type: ignore[arg-type]
                            int(message.values[2].tag)  # type: ignore[arg-type]
                        )
                    )
            elif message.dimension.tag == "13":
                for callback in cls._event_callbacks.get(LightEvents.WHITE_TEMP_CHANGE, []):
                    loop.create_task(
                        callback(
                            item,
                            int(message.values[0].tag)  # type: ignore[arg-type]
                        )
                    )
        elif isinstance(message, NormalMessage):
            for callback in cls._event_callbacks.get(LightEvents.STATUS_CHANGE, []):
                loop.create_task(
                    callback(
                        item,
                        message.what == WhatLight.ON
                    )
                )
        else:
            raise ValueError(f"Invalid message: {message}")
