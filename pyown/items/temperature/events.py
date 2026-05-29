"""Stub events + parser for the thermoregulation smoke test."""

from dataclasses import dataclass
from typing import Iterable

from ...events import Event, parser
from ...messages import BaseMessage, NormalMessage
from ...tags import Who
from ..base import BaseItem

__all__ = ["ThermoStatusEvent"]


@dataclass(frozen=True, slots=True)
class ThermoStatusEvent(Event):
    raw_what: str


@parser(Who.THERMOREGULATION)
def parse_thermo(item: BaseItem, message: BaseMessage) -> Iterable[Event]:
    if isinstance(message, NormalMessage):
        yield ThermoStatusEvent(item, item.where, raw_what=str(message.what))
