"""Typed events and parser for automation (WHO=2)."""

from dataclasses import dataclass
from typing import Iterable

from ...events import Event, parser
from ...messages import BaseMessage, NormalMessage
from ...tags import Who
from ..base import BaseItem
from .automation import WhatAutomation

__all__ = ["AutomationStatusEvent"]


@dataclass(frozen=True, slots=True)
class AutomationStatusEvent(Event):
    """The shutter/blind's state changed.

    Note: when an automation is already in a given state and the same command
    is sent, the gateway sometimes emits a STOP event followed by the requested
    direction. Subscribers should handle this.
    """

    state: WhatAutomation


@parser(Who.AUTOMATION)
def parse_automation(item: BaseItem, message: BaseMessage) -> Iterable[Event]:
    if isinstance(message, NormalMessage):
        yield AutomationStatusEvent(
            item, item.where, state=WhatAutomation(str(message.what))
        )
