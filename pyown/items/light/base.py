from enum import Enum, auto, StrEnum

from ..base import BaseItem
from ...tags import Who, What

__all__ = [
    "LightState",
    "BaseLight",
    "WhatLight",
]


class LightState(Enum):
    """The state of a light item."""
    OFF = auto()
    ON = auto()


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


class BaseLight(BaseItem):
    """Base class for all light items."""
    _who = Who.LIGHTING

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



