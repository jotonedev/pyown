"""Typed events and parser for gateway (WHO=13)."""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from ipaddress import IPv4Address
from typing import Iterable

from ...events import Event, parser
from ...messages import BaseMessage, DimensionResponse, DimensionWriting
from ...tags import Who
from ..base import BaseItem
from .gateway import Gateway, GatewayModel, WhatGateway

__all__ = [
    "GatewayTimeEvent",
    "GatewayDateEvent",
    "GatewayIPEvent",
    "GatewayNetmaskEvent",
    "GatewayMacAddressEvent",
    "GatewayModelEvent",
    "GatewayFirmwareEvent",
    "GatewayUptimeEvent",
    "GatewayDateTimeEvent",
    "GatewayKernelVersionEvent",
    "GatewayDistributionVersionEvent",
]


@dataclass(frozen=True, slots=True)
class GatewayTimeEvent(Event):
    time: time


@dataclass(frozen=True, slots=True)
class GatewayDateEvent(Event):
    date: date


@dataclass(frozen=True, slots=True)
class GatewayIPEvent(Event):
    ip: IPv4Address


@dataclass(frozen=True, slots=True)
class GatewayNetmaskEvent(Event):
    netmask: str


@dataclass(frozen=True, slots=True)
class GatewayMacAddressEvent(Event):
    mac: str


@dataclass(frozen=True, slots=True)
class GatewayModelEvent(Event):
    model: GatewayModel


@dataclass(frozen=True, slots=True)
class GatewayFirmwareEvent(Event):
    version: str


@dataclass(frozen=True, slots=True)
class GatewayUptimeEvent(Event):
    uptime: timedelta


@dataclass(frozen=True, slots=True)
class GatewayDateTimeEvent(Event):
    datetime: datetime


@dataclass(frozen=True, slots=True)
class GatewayKernelVersionEvent(Event):
    version: str


@dataclass(frozen=True, slots=True)
class GatewayDistributionVersionEvent(Event):
    version: str


_DISPATCH = {
    WhatGateway.TIME.value: lambda i, m: GatewayTimeEvent(i, i.where, time=Gateway._decode_time(m)),
    WhatGateway.DATE.value: lambda i, m: GatewayDateEvent(i, i.where, date=Gateway._decode_date(m)),
    WhatGateway.IP_ADDRESS.value: lambda i, m: GatewayIPEvent(i, i.where, ip=Gateway._decode_ip(m)),
    WhatGateway.NET_MASK.value: lambda i, m: GatewayNetmaskEvent(
        i, i.where, netmask=Gateway._decode_netmask(m)
    ),
    WhatGateway.MAC_ADDRESS.value: lambda i, m: GatewayMacAddressEvent(
        i, i.where, mac=Gateway._decode_macaddress(m)
    ),
    WhatGateway.DEVICE_TYPE.value: lambda i, m: GatewayModelEvent(
        i, i.where, model=Gateway._decode_model(m)
    ),
    WhatGateway.FIRMWARE_VERSION.value: lambda i, m: GatewayFirmwareEvent(
        i, i.where, version=Gateway._decode_version_triplet(m)
    ),
    WhatGateway.UPTIME.value: lambda i, m: GatewayUptimeEvent(
        i, i.where, uptime=Gateway._decode_uptime(m)
    ),
    WhatGateway.DATE_TIME.value: lambda i, m: GatewayDateTimeEvent(
        i, i.where, datetime=Gateway._decode_datetime(m)
    ),
    WhatGateway.KERNEL_VERSION.value: lambda i, m: GatewayKernelVersionEvent(
        i, i.where, version=Gateway._decode_version_triplet(m)
    ),
    WhatGateway.DISTRIBUTION_VERSION.value: lambda i, m: GatewayDistributionVersionEvent(
        i, i.where, version=Gateway._decode_version_triplet(m)
    ),
}


@parser(Who.GATEWAY)
def parse_gateway(item: BaseItem, message: BaseMessage) -> Iterable[Event]:
    if isinstance(message, DimensionWriting) and not isinstance(message, DimensionResponse):
        # Some gateways report changes via DimensionWriting framing; treat the
        # two interchangeably for the purposes of event parsing.
        msg: DimensionResponse | DimensionWriting = message
    elif isinstance(message, DimensionResponse):
        msg = message
    else:
        return

    builder = _DISPATCH.get(msg.dimension.string)
    if builder is None:
        return
    yield builder(item, msg)
