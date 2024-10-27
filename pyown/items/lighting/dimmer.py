from typing import Callable, Self, Coroutine, AsyncIterator

from .base import BaseLight, WhatLight, LightEvents
from ...tags import Value, Dimension
from ...tags import Where

__all__ = [
    "Dimmer",
]


class Dimmer(BaseLight):
    """
    Dimmer items are items that can have their brightness level changed or colors changed.
    """

    async def turn_on(self, speed: int | None = None):
        """
        Turns the light on.

        Args:
            speed: turn on the light with a specific speed [0-255]
        """
        if speed is not None and (speed < 0 or speed > 255):
            raise ValueError("Invalid speed value")

        what = WhatLight.ON
        # I do not own a dimmer, so I cannot test this.
        # Also, the documentation is not clear on what is the range of the speed parameter
        if speed is not None:
            what = what.with_parameter(speed)
        await self.send_normal_message(what)

    async def turn_off(self, speed: int | None = None):
        """
        Turns the light off.

        Args:
            speed: turn off the light with a specific speed [0-255]
        """
        if speed is not None and (speed < 0 or speed > 255):
            raise ValueError("Invalid speed value")

        what = WhatLight.OFF

        if speed is not None:
            what = what.with_parameter(speed)
        await self.send_normal_message(what)

    async def set_20_percent(self):
        """Sets the light to 20%."""
        await self.send_normal_message(WhatLight.ON_20_PERCENT)

    async def set_30_percent(self):
        """Sets the light to 30%."""
        await self.send_normal_message(WhatLight.ON_30_PERCENT)

    async def set_40_percent(self):
        """Sets the light to 40%."""
        await self.send_normal_message(WhatLight.ON_40_PERCENT)

    async def set_50_percent(self):
        """Sets the light to 50%."""
        await self.send_normal_message(WhatLight.ON_50_PERCENT)

    async def set_60_percent(self):
        """Sets the light to 60%."""
        await self.send_normal_message(WhatLight.ON_60_PERCENT)

    async def set_70_percent(self):
        """Sets the light to 70%."""
        await self.send_normal_message(WhatLight.ON_70_PERCENT)

    async def set_80_percent(self):
        """Sets the light to 80%."""
        await self.send_normal_message(WhatLight.ON_80_PERCENT)

    async def set_90_percent(self):
        """Sets the light to 90%."""
        await self.send_normal_message(WhatLight.ON_90_PERCENT)

    async def set_100_percent(self):
        """Sets the light to 100%."""
        await self.send_normal_message(WhatLight.ON_100_PERCENT)

    async def up_percent(
            self,
            value: int | None = None,
            speed: int | None = None
    ):
        """
        Increases the light percentage.

        Args:
            value: the percentage to increase, by default, 1
            speed: increase the light percentage with a specific speed [0-255]
        """
        if value is not None and (value < 0 or value > 100):
            raise ValueError("Invalid value")

        what = WhatLight.UP_1_PERCENT

        if value is not None:
            what = what.with_parameter(value)
        if speed is not None:
            what = what.with_parameter(speed)

        await self.send_normal_message(what)

    async def down_percent(
            self,
            value: int | None = None,
            speed: int | None = None
    ):
        """
        Decreases the light percentage.

        Args:
            value: the percentage to decrease, by default 1
            speed: decrease the light percentage with a specific speed [0-255]
        """
        if value is not None and (value < 0 or value > 100):
            raise ValueError("Invalid value")

        what = WhatLight.DOWN_1_PERCENT

        if value is not None:
            what = what.with_parameter(value)
        if speed is not None:
            what = what.with_parameter(speed)

        await self.send_normal_message(what)

    async def get_status(self) -> AsyncIterator[tuple[Where, int]]:
        """
        Gets the status of the light.

        Yields:
            tuple[Where, int]: the first element is the location of the light,
            the second is the brightness level [0-100]
        """
        async for message in self.send_status_request():
            yield message.where, int(message.what.tag) * 10  # type: ignore[arg-type]

    async def set_brightness_with_speed(self, brightness: int | str, speed: int | str):
        """
        Sets the brightness of the light with a specific speed.

        Args:
            brightness: the brightness to set
            speed: the speed to set the brightness
        """
        await self.send_dimension_writing(Dimension("1"), Value(brightness), Value(speed))

    async def set_hsv(self, hue: int, saturation: int, value: int):
        """
        Sets the color of the light in HSV format.

        Args:
            hue: the hue value to set [0-359]
            saturation: the saturation value [0-100]
            value:  the value to set [0-100]
        """
        if hue < 0 or hue > 359:
            raise ValueError("Invalid hue value")

        if saturation < 0 or saturation > 100:
            raise ValueError("Invalid saturation value")

        if value < 0 or value > 100:
            raise ValueError("Invalid value")

        await self.send_dimension_writing("12", Value(hue), Value(saturation), Value(value))

    async def set_white_temperature(self, temperature: int):
        """
        Sets the white temperature of the light.

        Args:
            temperature: the temperature to set [1-65534] using the Mired scale.
        """
        if temperature < 1 or temperature > 65534:
            raise ValueError("Invalid temperature value")

        await self.send_dimension_writing("13", Value(temperature))

    async def request_current_brightness_speed(self) -> AsyncIterator[tuple[Where, int, int]]:
        """
        Requests the current brightness and speed of the light.

        Yields:
            A tuple with the where of the item, its brightness level, and its current speed.
            The speed is in the range [0-255].
            The brightness is in the range [100-200].
        """
        async for message in self.send_dimension_request("1"):
            brightness = int(message.values[0].tag)  # type: ignore[arg-type]
            speed = int(message.values[1].tag)  # type: ignore[arg-type]
            yield message.where, brightness, speed

    async def request_current_hsv(self) -> AsyncIterator[tuple[Where, int, int, int]]:
        """
        Requests the current HSV of the light, valid only for RGB lights.

        Yields:
            A tuple with the where of the item, the hue, the saturation, and the value.
                The hue is in the range [0-359].
                The saturation is in the range [0-100].
                The value is in the range [0-100].
        """
        async for message in self.send_dimension_request("12"):
            hue = int(message.values[0].tag)  # type: ignore[arg-type]
            saturation = int(message.values[1].tag)  # type: ignore[arg-type]
            value = int(message.values[2].tag)  # type: ignore[arg-type]
            yield message.where, hue, saturation, value

    async def request_current_white_temperature(self) -> AsyncIterator[tuple[Where, int]]:
        """
        Requests the current white temperature of the light.

        Yields:
            The where of the item and the temperature.
                The temperature is in the range [1-65534] using the Mired scale.
        """
        async for message in self.send_dimension_request("14"):
            yield message.where, int(message.values[0].tag)  # type: ignore[arg-type]

    @classmethod
    def on_luminosity_change(cls, callback: Callable[[Self, int, int], Coroutine[None, None, None]]):
        """
        Registers a callback function to be called when the luminosity changes.

        Args:
            callback: The callback function to call.
                It will receive as arguments the item, dimmer level and speed
        """
        cls._event_callbacks.setdefault(LightEvents.LUMINOSITY_CHANGE, []).append(callback)

    @classmethod
    def on_hsv_change(cls, callback: Callable[[Self, int, int, int], Coroutine[None, None, None]]):
        """
        Registers a callback function to be called when the HSV changes.

        Args:
            callback: The callback function to call.
                It will receive as arguments the item, the hue, the saturation, and the value.
        """
        cls._event_callbacks.setdefault(LightEvents.HSV_CHANGE, []).append(callback)

    @classmethod
    def on_white_temp_change(cls, callback: Callable[[Self, int], Coroutine[None, None, None]]):
        """
        Registers a callback function to be called when the white temperature changes.

        Args:
            callback: The callback function to call.
                It will receive as arguments the item and the temperature.
        """
        cls._event_callbacks.setdefault(LightEvents.WHITE_TEMP_CHANGE, []).append(callback)
