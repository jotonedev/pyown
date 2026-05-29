"""Typed events and parser for cameras / video door entry (WHO=7)."""

from dataclasses import dataclass
from typing import Iterable

from ...events import Event, parser
from ...messages import BaseMessage, NormalMessage
from ...tags import Who
from ..base import BaseItem
from .camera import WhatCamera

__all__ = ["CameraStatusEvent"]


@dataclass(frozen=True, slots=True)
class CameraStatusEvent(Event):
    """Generic camera state change.

    Camera commands cover a broad surface (zoom, brightness, dial display, …)
    and most do not have a meaningful structured payload — they only signal
    that *something* happened. We surface the WHAT value as `command` and
    leave the raw message attached for callers who need more detail.
    """

    command: WhatCamera
    message: BaseMessage


@parser(Who.VIDEO_DOOR_ENTRY)
def parse_camera(item: BaseItem, message: BaseMessage) -> Iterable[Event]:
    if isinstance(message, NormalMessage):
        yield CameraStatusEvent(
            item, item.where,
            command=WhatCamera(str(message.what)),
            message=message,
        )
