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
    "GatewayModel",
]


class GatewayModel(StrEnum):
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
    

EventMessage = DimensionResponse | DimensionWriting | None


class Gateway(BaseItem):
    _who = Who.GATEWAY

    _event_callbacks: dict[WhatGateway, list[CoroutineCallback]] = {}
    
    async def _single_dim_req(self, what: WhatGateway) -> EventMessage:
        messages = [msg async for msg in self.send_dimension_request(what)]

        resp = messages[0]
        if not isinstance(resp, DimensionResponse):
            raise InvalidMessage("The message is not a DimensionResponse message.")
        else:
            return resp

    async def get_time(self, *, message: EventMessage = None) -> datetime.time:
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
            resp = self._single_dim_req(WhatGateway.TIME)

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

    # noinspection DuplicatedCode
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

    async def get_date(self, *, message: EventMessage = None) -> datetime.date:
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
            resp = self._single_dim_req(WhatGateway.DATE)

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

    async def get_ip(self, *, message: EventMessage = None) -> ipaddress.IPv4Address:
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
            resp = self._single_dim_req(WhatGateway.IP_ADDRESS)

        oct1, oct2, oct3, oct4 = resp.values

        ip = ipaddress.IPv4Address(f"{int(oct1.string)}.{int(oct2.string)}.{int(oct3.string)}.{int(oct4.string)}")
        return ip

    async def get_netmask(self, *, message: EventMessage = None) -> str:
        """
        Requests the net mask of the gateway.

        Args:
            message: The message to parse the net mask from. If not provided, send a request to the gateway.
                It's used by call_callbacks to parse the message.

        Returns:
            str: The net mask of the gateway.
        """
        if message is not None:
            resp = message
        else:
            resp = self._single_dim_req(WhatGateway.NET_MASK)

        oct1, oct2, oct3, oct4 = resp.values

        return f"{int(oct1.string)}.{int(oct2.string)}.{int(oct3.string)}.{int(oct4.string)}"

    async def get_macaddress(self, *, message: EventMessage = None) -> str:
        """
        Requests the MAC address of the gateway.

        Args:
            message: The message to parse the MAC address from. If not provided, send a request to the gateway.
                It's used by call_callbacks to parse the message.

        Returns:
            str: The MAC address of the gateway.
        """
        if message is not None:
            resp = message
        else:
            resp = self._single_dim_req(WhatGateway.MAC_ADDRESS)

        oct1, oct2, oct3, oct4, oct5, oct6 = resp.values

        mac = f"{oct1.string}:{oct2.string}:{oct3.string}:{oct4.string}:{oct5.string}:{oct6.string}"
        return mac

    async def get_netinfo(self) -> ipaddress.IPv4Network:
        """
        Combines the net mask and the IP address to get the network info.
        Returns:
            ipaddress.IPv4Network: The network info.
        """
        ip = await self.get_ip()
        netmask = await self.get_netmask()

        return ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)

    async def get_model(self, *, message: EventMessage = None) -> GatewayModel:
        """
        Requests the device type of the gateway.

        Args:
            message: The message to parse the device type from. If not provided, send a request to the gateway.
                It's used by call_callbacks to parse the message.

        Returns:
            GatewayModel: The device type of the gateway.
        """
        if message is not None:
            resp = message
        else:
            resp = self._single_dim_req(WhatGateway.DEVICE_TYPE)

        return GatewayModel(resp.values[0].string)

    async def get_firmware(self, *, message: EventMessage = None) -> str:
        """
        Requests the firmware version of the gateway.

        Args:
            message: The message to parse the firmware version from. If not provided, send a request to the gateway.
                It's used by call_callbacks to parse the message.

        Returns:
            str: The firmware version of the gateway.
        """
        if message is not None:
            resp = message
        else:
            resp = self._single_dim_req(WhatGateway.FIRMWARE_VERSION)

        v = resp.values[0].string
        r = resp.values[1].string
        b = resp.values[2].string

        return f"{v}.{r}.{b}"

    async def get_uptime(self, *, message: EventMessage = None) -> datetime.timedelta:
        """
        Requests the uptime of the gateway.

        Args:
            message: The message to parse the uptime from. If not provided, send a request to the gateway.
                It's used by call_callbacks to parse the message.

        Returns:
            datetime.timedelta: The uptime of the gateway.
        """
        if message is not None:
            resp = message
        else:
            resp = self._single_dim_req(WhatGateway.UPTIME)

        d = int(resp.values[0].string)
        h = int(resp.values[1].string)
        m = int(resp.values[2].string)
        s = int(resp.values[3].string)

        uptime = datetime.timedelta(days=d, hours=h, minutes=m, seconds=s)
        return uptime

    async def get_datetime(self, *, message: EventMessage = None) -> datetime.datetime:
        """
        Requests the date and time of the gateway.

        Args:
            message: The message to parse the date and time from. If not provided, send a request to the gateway.
                It's used by call_callbacks to parse the message.

        Returns:
            datetime.datetime: The date and time of the gateway.
        """
        if message is not None:
            resp = message
        else:
            resp = self._single_dim_req(WhatGateway.DATE_TIME)

        h = int(resp.values[0].string)
        m = int(resp.values[1].string)
        s = int(resp.values[2].string)
        t = resp.values[3].string

        w = int(resp.values[4].string)
        d = int(resp.values[5].string)
        mo = int(resp.values[6].string)
        y = int(resp.values[7].string)

        # the timezone is in the format 001 where the first digit is the sign and the last two digits are the hours
        sign = t[0]
        hours = int(t[1:3])

        # parse the time with the timezone
        bus_time = datetime.datetime(
            y, mo, d, h, m, s,
            tzinfo=datetime.timezone(
                datetime.timedelta(hours=hours) if sign == "0" else -datetime.timedelta(hours=hours)
            )
        )

        return bus_time

    # noinspection DuplicatedCode
    async def set_datetime(self, bus_time: datetime.datetime):
        """
        Sets the date and time of the gateway.
        Args:
            bus_time: the date and time to set with the timezone.

        Returns:
            None
        """
        sign = "0" if bus_time.tzinfo.utcoffset(None) >= datetime.timedelta(0) else "1"
        hours = abs(bus_time.tzinfo.utcoffset(None).seconds) // 3600

        t = Value(f"{sign}{hours:03d}")
        h = Value(f"{bus_time.hour:02d}")
        m = Value(f"{bus_time.minute:02d}")
        s = Value(f"{bus_time.second:02d}")

        d = Value(f"{bus_time.day:02d}")
        mo = Value(f"{bus_time.month:02d}")
        y = Value(f"{bus_time.year}")

        await self.send_dimension_writing(WhatGateway.DATE_TIME, h, m, s, t, d, mo, y)

    async def get_kernel_version(self, *, message: EventMessage = None) -> str:
        """
        Requests the linux kernel version of the gateway.

        Args:
            message: The message to parse the kernel version from. If not provided, send a request to the gateway.
                It's used by call_callbacks to parse the message.

        Returns:
            str: The linux kernel version used by the gateway.
        """
        if message is not None:
            resp = message
        else:
            resp = self._single_dim_req(WhatGateway.KERNEL_VERSION)

        v = resp.values[0].string
        r = resp.values[1].string
        b = resp.values[2].string

        return f"{v}.{r}.{b}"

    async def get_distribution_version(self, *, message: EventMessage = None) -> str:
        """
        Requests the os distribution version of the gateway.

        Args:
            message: The message to parse the distribution version from. If not provided, send a request to the gateway.
                It's used by call_callbacks to parse the message.

        Returns:
            str: The os distribution version used by the gateway.
        """
        if message is not None:
            resp = message
        else:
            resp = self._single_dim_req(WhatGateway.DISTRIBUTION_VERSION)

        v = resp.values[0].string
        r = resp.values[1].string
        b = resp.values[2].string

        return f"{v}.{r}.{b}"

    @classmethod
    def call_callbacks(cls, item: Self, message: BaseMessage) -> list[Task]:
        pass