from .base import BaseLight, WhatLight
from ...tags import Value, Dimension

__all__ = [
    "Dimmer",
]


class Dimmer(BaseLight):
    async def turn_on(self, speed: int | None = None):
        """
        Turn the light on.

        Args:
            speed: turn on the light with a specific speed
        """
        what = WhatLight.ON
        # I do not own a dimmer, so I cannot test this.
        # Also, the documentation is not clear on what is the range of the speed parameter
        if speed is not None:
            what = what.with_parameters(speed)
        await self.send_normal_message(what)

    async def turn_off(self, speed: int | None = None):
        """
        Turn the light off.

        Args:
            speed: turn off the light with a specific speed
        """
        what = WhatLight.OFF

        if speed is not None:
            what = what.with_parameters(speed)
        await self.send_normal_message(what)

    async def set_20_percent(self):
        """Set the light to 20%."""
        await self.send_normal_message(WhatLight.ON_20_PERCENT)

    async def set_30_percent(self):
        """Set the light to 30%."""
        await self.send_normal_message(WhatLight.ON_30_PERCENT)

    async def set_40_percent(self):
        """Set the light to 40%."""
        await self.send_normal_message(WhatLight.ON_40_PERCENT)

    async def set_50_percent(self):
        """Set the light to 50%."""
        await self.send_normal_message(WhatLight.ON_50_PERCENT)

    async def set_60_percent(self):
        """Set the light to 60%."""
        await self.send_normal_message(WhatLight.ON_60_PERCENT)

    async def set_70_percent(self):
        """Set the light to 70%."""
        await self.send_normal_message(WhatLight.ON_70_PERCENT)

    async def set_80_percent(self):
        """Set the light to 80%."""
        await self.send_normal_message(WhatLight.ON_80_PERCENT)

    async def set_90_percent(self):
        """Set the light to 90%."""
        await self.send_normal_message(WhatLight.ON_90_PERCENT)

    async def set_100_percent(self):
        """Set the light to 100%."""
        await self.send_normal_message(WhatLight.ON_100_PERCENT)

    async def up_percent(
            self,
            value: int | None = None,
            speed: int | None = None
    ):
        """
        Increase the light percentage.

        Args:
            value: the percentage to increase, by default 1
            speed: increase the light percentage with a specific speed
        """
        what = WhatLight.UP_1_PERCENT

        if value is not None:
            what = what.with_parameters(value)
        if speed is not None:
            what = what.with_parameters(speed)

        await self.send_normal_message(what)

    async def down_percent(
            self,
            value: int | None = None,
            speed: int | None = None
    ):
        """
        Decrease the light percentage.

        Args:
            value: the percentage to decrease, by default 1
            speed: decrease the light percentage with a specific speed
        """
        what = WhatLight.DOWN_1_PERCENT

        if value is not None:
            what = what.with_parameters(value)
        if speed is not None:
            what = what.with_parameters(speed)

        await self.send_normal_message(what)

    async def get_status(self) -> int:
        """
        Get the status of the light.

        Returns:
            True if the light is on, False if the light is off.
        """
        resp = await self.send_status_request()

        return int(resp.what.tag)

    async def set_brightness_with_speed(self, brightness: int | str, speed: int | str):
        """
        Set the brightness of the light with a specific speed.

        Args:
            brightness: the brightness to set
            speed: the speed to set the brightness

        Raises:
            RequestError: If the server does not acknowledge the message.
        """
        if isinstance(brightness, int):
            brightness = str(brightness)

        if isinstance(speed, int):
            speed = str(speed)

        await self.send_dimension_writing(Dimension("1"), Value(brightness), Value(speed))

    async def set_hsv(self, hue: int, saturation: int, value: int):
        """
        Set the color of the light in HSV format.

        Args:
            hue: the hue value
            saturation: the saturation value
            value:  the value to set
        """
        if hue < 0 or hue > 360:
            raise ValueError("Invalid hue value")

        if saturation < 0 or saturation > 100:
            raise ValueError("Invalid saturation value")

        if value < 0 or value > 100:
            raise ValueError("Invalid value")

        hue = Value(str(hue))
        saturation = Value(str(saturation))
        value = Value(str(value))

        await self.send_dimension_writing("12", hue, saturation, value)

    async def set_white_temperature(self, temperature: int):
        """
        Set the white temperature of the light.

        Args:
            temperature: the temperature to set
        """
        # It's not clear what is the range of the temperature parameter
        temperature = Value(str(temperature))

        await self.send_dimension_writing("13", temperature)

    async def request_current_brightness_speed(self):
        """
        Request the gateway the last set brightness and speed command that was sent.

        The response will be sent to the event session.
        """
        msg = self.create_dimension_request_message(Dimension("2"))
        await self._send_message(msg)

        resp = await self._read_message()
        self._check_ack(resp)

    async def request_current_hsv(self):
        """
        Request the gateway the last set HSV command that was sent.

        The response will be sent to the event session.
        """
        msg = self.create_dimension_request_message(Dimension("12"))
        await self._send_message(msg)

        resp = await self._read_message()
        self._check_ack(resp)

    async def request_current_white_temperature(self):
        """
        Request the gateway the last set white temperature command that was sent.

        The response will be sent to the event session.
        """
        msg = self.create_dimension_request_message(Dimension("14"))
        await self._send_message(msg)

        resp = await self._read_message()
        self._check_ack(resp)
