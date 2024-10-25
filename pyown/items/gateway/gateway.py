import time
import datetime
import ipaddress

from abc import ABC, abstractmethod
from asyncio import Task
from enum import StrEnum, Enum, auto
from typing import Callable, Self, Coroutine, AsyncIterator

from ..base import BaseItem, CoroutineCallback
from ...exceptions import InvalidMessage
from ...messages import DimensionResponse, BaseMessage, NormalMessage, DimensionWriting
from ...tags import Who, What, Value, Where


__all__ = [
    "Gateway",
    "WhatGateway",
    "GatewayType",
]


class GatewayType(StrEnum):
    """
    This enum is used to define the various models of gateways that are supported by the library.

    This is not a complete list of all the gateways, because there are many different models of gateways that are not
    listed in the official documentation. So, if you have a gateway that is not listed here, you can send an issue
    on GitHub.

    Attributes:
        MHServer:
        MH200:
        F452:
        F452V:
        MHServer2:
        H4684:
    """
    MHServer = "2"
    MH200 = "4"
    F452 = "6"
    F452V = "7"
    MHServer2 = "11"
    H4684 = "12"


class WhatGateway(What, StrEnum):
    """
    This enum is used to define the various types of data that can be retrieved from a gateway.

    Attributes:
        TIME: get or set the time of the gateway and bus.
        DATE: get or set the date of the gateway and bus.
        IP_ADDRESS: get the IP address of the gateway.
        NET_MASK: get the net mask of the gateway.
        MAC_ADDRESS: get the MAC address of the gateway.
        DEVICE_TYPE: get the device type of the gateway.
        FIRMWARE_VERSION: get the firmware version of the gateway.
        UPTIME: get the uptime of the gateway.
        DATE_TIME: get or set the date and time of the gateway.
        KERNEL_VERSION: get the linux kernel version of the gateway.
        DISTRIBUTION_VERSION: get the linux distribution version of the gateway.
    """
    TIME: str = "0"
    DATE: str = "1"
    IP_ADDRESS: str = "10"
    NET_MASK: str = "11"
    MAC_ADDRESS: str = "12"
    DEVICE_TYPE: str = "15"
    FIRMWARE_VERSION: str = "16"
    UPTIME: str = "19"
    DATE_TIME: str = "22"
    KERNEL_VERSION: str = "23"
    DISTRIBUTION_VERSION: str = "24"


class Gateway(BaseItem):
    _who = Who.GATEWAY

    _event_callbacks: dict[WhatGateway, list[CoroutineCallback]] = {}

    async def get_time(self, *, message: DimensionResponse | DimensionWriting | None = None) -> datetime.time:
        """
        Requests the time of the gateway and bus.

        Args:
            message: The message to parse the time from. If not provided, send a request to the gateway.
                It's used by call_callbacks to parse the message.

        Returns:
            datetime.time: The time of the gateway and bus.
        """
        if message is not None:
            resp = message
        else:
            messages = [msg async for msg in self.send_dimension_request(WhatGateway.TIME)]

            resp = messages[0]
            if not isinstance(resp, DimensionResponse):
                raise InvalidMessage("The message is not a DimensionResponse message.")

        h_v, m_v, s_v, t_v = resp.values
        # the timezone is in the format 001 where the first digit is the sign and the last two digits are the hours
        sign = t_v.string[0]
        hours = int(t_v.string[1:3])

        h = int(h_v.string)
        m = int(m_v.string)
        s = int(s_v.string)

        # parse the time with the timezone
        bus_time = datetime.time(
            h,
            m,
            s,
            tzinfo=datetime.timezone(
                datetime.timedelta(hours=hours) if sign == "0" else -datetime.timedelta(hours=hours)
            )
        )

        return bus_time

    async def set_time(self, bus_time: datetime.time):
        """
        Sets the time of the gateway and bus.
        Args:
            bus_time: the time to set with the timezone.

        Returns:
            None
        """
        sign = "0" if bus_time.tzinfo.utcoffset(None) >= datetime.timedelta(0) else "1"
        hours = abs(bus_time.tzinfo.utcoffset(None).seconds) // 3600

        t = Value(f"{sign}{hours:03d}")
        h = Value(f"{bus_time.hour:02d}")
        m = Value(f"{bus_time.minute:02d}")
        s = Value(f"{bus_time.second:02d}")

        await self.send_dimension_writing(WhatGateway.TIME, h, m, s, t)

    async def get_date(self, *, message: DimensionResponse | DimensionWriting | None = None) -> datetime.date:
        """
        Requests the date of the gateway and bus.

        Args:
            message: The message to parse the date from. If not provided, send a request to the gateway.
                It's used by call_callbacks to parse the message.

        Returns:
            datetime.date: The date of the gateway and bus.
        """
        if message is not None:
            resp = message
        else:
            messages = [msg async for msg in self.send_dimension_request(WhatGateway.DATE)]

            resp = messages[0]
            if not isinstance(resp, DimensionResponse):
                raise InvalidMessage("The message is not a DimensionResponse message.")

        w, d, m, a = resp.values
        # w is the day of the week, but we don't need it

        day = int(d.string)
        month = int(m.string)
        year = int(a.string)

        bus_date = datetime.date(year, month, day)

        return bus_date

    async def set_date(self, bus_date: datetime.date):
        """
        Sets the date of the gateway and bus.
        Args:
            bus_date: the date to set.

        Returns:
            None
        """
        d = Value(f"{bus_date.day:02d}")
        m = Value(f"{bus_date.month:02d}")
        a = Value(f"{bus_date.year}")
        # calculate the day of the week, 00 is Sunday
        if bus_date.weekday() == 6:
            w = Value("00")
        else:
            w = Value(f"{bus_date.weekday()+1:02d}")

        await self.send_dimension_writing(WhatGateway.DATE, w, d, m, a)

    async def get_ip(self, *, message: DimensionResponse | DimensionWriting | None = None) -> ipaddress.IPv4Address:
        """
        Requests the IP address of the gateway.

        Args:
            message: The message to parse the IP address from. If not provided, send a request to the gateway.
                It's used by call_callbacks to parse the message.

        Returns:
            ipaddress.IPv4Address: The IP address of the gateway.
        """
        if message is not None:
            resp = message
        else:
            messages = [msg async for msg in self.send_dimension_request(WhatGateway.IP_ADDRESS)]

            resp = messages[0]
            if not isinstance(resp, DimensionResponse):
                raise InvalidMessage("The message is not a DimensionResponse message.")

        oct1, oct2, oct3, oct4 = resp.values

        ip = ipaddress.IPv4Address(f"{int(oct1.string)}.{int(oct2.string)}.{int(oct3.string)}.{int(oct4.string)}")
        return ip


    @classmethod
    def call_callbacks(cls, item: Self, message: BaseMessage) -> list[Task]:
        pass