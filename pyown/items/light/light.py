from .base import BaseLight, WhatLight

__all__ = [
    "Light",
]


class Light(BaseLight):
    async def turn_on(self):
        """Turn the light on."""
        await self.send_normal_message(WhatLight.ON)

    async def turn_off(self):
        """Turn the light off."""
        await self.send_normal_message(WhatLight.OFF)

    async def blink_0_5_sec(self):
        """Blink the light every 0.5 seconds."""
        await self.send_normal_message(WhatLight.BLINKING_0_5_SEC)

    async def blink_1_0_sec(self):
        """Blink the light every 1.0 seconds."""
        await self.send_normal_message(WhatLight.BLINKING_1_0_SEC)

    async def blink_1_5_sec(self):
        """Blink the light every 1.5 seconds."""
        await self.send_normal_message(WhatLight.BLINKING_1_5_SEC)

    async def blink_2_0_sec(self):
        """Blink the light every 2.0 seconds."""
        await self.send_normal_message(WhatLight.BLINKING_2_0_SEC)

    async def blink_2_5_sec(self):
        """Blink the light every 2.5 seconds."""
        await self.send_normal_message(WhatLight.BLINKING_2_5_SEC)

    async def blink_3_0_sec(self):
        """Blink the light every 3.0 seconds."""
        await self.send_normal_message(WhatLight.BLINKING_3_0_SEC)

    async def blink_3_5_sec(self):
        """Blink the light every 3.5 seconds."""
        await self.send_normal_message(WhatLight.BLINKING_3_5_SEC)

    async def blink_4_0_sec(self):
        """Blink the light every 4.0 seconds."""
        await self.send_normal_message(WhatLight.BLINKING_4_0_SEC)

    async def blink_4_5_sec(self):
        """Blink the light every 4.5 seconds."""
        await self.send_normal_message(WhatLight.BLINKING_4_5_SEC)

    async def blink_5_0_sec(self):
        """Blink the light every 5.0 seconds."""
        await self.send_normal_message(WhatLight.BLINKING_5_0_SEC)

    async def get_status(self) -> bool:
        """
        Get the status of the light.

        Returns:
            True if the light is on, False if the light is off.
        """
        resp = await self.send_status_request()

        return resp.what == WhatLight.ON
