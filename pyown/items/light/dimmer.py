from .base import BaseLight, WhatLight

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
