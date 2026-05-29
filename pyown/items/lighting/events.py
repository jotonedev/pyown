"""Typed events and parser for lighting (WHO=1)."""

from dataclasses import dataclass
from typing import Iterable

from ...events import Event, parser
from ...messages import BaseMessage, DimensionResponse, NormalMessage
from ...tags import Who
from ..base import BaseItem
from .base import WhatLight

__all__ = [
    "LightStatusEvent",
    "LightLuminosityEvent",
    "LightTemporizationEvent",
    "LightHSVEvent",
    "LightWhiteTempEvent",
]


@dataclass(frozen=True, slots=True)
class LightStatusEvent(Event):
    """The light's on/off state changed."""

    on: bool


@dataclass(frozen=True, slots=True)
class LightLuminosityEvent(Event):
    """The dimmer's luminosity changed (dimension 8 / dimension 1)."""

    luminosity: int
    speed: int


@dataclass(frozen=True, slots=True)
class LightTemporizationEvent(Event):
    """The light's temporization (auto-off timer) changed (dimension 2)."""

    hour: int
    minute: int
    second: int


@dataclass(frozen=True, slots=True)
class LightHSVEvent(Event):
    """The RGB light's color changed (dimension 12)."""

    hue: int
    saturation: int
    value: int


@dataclass(frozen=True, slots=True)
class LightWhiteTempEvent(Event):
    """The light's white temperature changed (dimension 13)."""

    temperature: int


@parser(Who.LIGHTING)
def parse_lighting(item: BaseItem, message: BaseMessage) -> Iterable[Event]:
    if isinstance(message, NormalMessage):
        yield LightStatusEvent(item, item.where, on=(str(message.what) == WhatLight.ON.value))
        return

    if isinstance(message, DimensionResponse):
        tag = message.dimension.tag
        vals = message.values
        if tag == "1":
            yield LightLuminosityEvent(
                item, item.where,
                luminosity=int(vals[0].tag),  # type: ignore[arg-type]
                speed=int(vals[1].tag),  # type: ignore[arg-type]
            )
        elif tag == "2":
            yield LightTemporizationEvent(
                item, item.where,
                hour=int(vals[0].tag),  # type: ignore[arg-type]
                minute=int(vals[1].tag),  # type: ignore[arg-type]
                second=int(vals[2].tag),  # type: ignore[arg-type]
            )
        elif tag == "8":
            yield LightLuminosityEvent(
                item, item.where,
                luminosity=int(vals[0].tag),  # type: ignore[arg-type]
                speed=int(vals[1].tag),  # type: ignore[arg-type]
            )
        elif tag == "12":
            yield LightHSVEvent(
                item, item.where,
                hue=int(vals[0].tag),  # type: ignore[arg-type]
                saturation=int(vals[1].tag),  # type: ignore[arg-type]
                value=int(vals[2].tag),  # type: ignore[arg-type]
            )
        elif tag == "13":
            yield LightWhiteTempEvent(
                item, item.where,
                temperature=int(vals[0].tag),  # type: ignore[arg-type]
            )
