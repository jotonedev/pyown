from enum import StrEnum
from typing import AsyncIterator

from ...events import item
from ...tags import What, Who
from ...tags.where import Where
from ..base import BaseItem

__all__ = [
    "Automation",
    "WhatAutomation",
]


class WhatAutomation(What, StrEnum):
    """The possible WHAT values for automation commands and states.

    Attributes:
        STOP: The command to stop the automation.
        UP: The command to go up.
        DOWN: The command to go down.
    """

    STOP = "0"
    UP = "1"
    DOWN = "2"


@item(Who.AUTOMATION)
class Automation(BaseItem):
    """Automation items are usually used to control blinds, shutters, etc."""

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
        """Requests the status of the automation.

        Raises:
            AttributeError: If the automation is not a light point.

        Returns:
            WhatAutomation: The status of the automation.
        """
        async for message in self.send_status_request():
            yield message.where, WhatAutomation(str(message.what))
