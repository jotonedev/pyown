import datetime
import ipaddress
import logging
from enum import StrEnum

from ...client import BaseClient
from ...events import item
from ...messages import DimensionResponse, DimensionWriting
from ...tags import Value, What, Where, Who
from ..base import BaseItem, EventMessage

__all__ = [
    "Gateway",
    "WhatGateway",
    "GatewayModel",
]


log = logging.getLogger("pyown.items.gateway")


class GatewayModel(StrEnum):
    """Models of gateways supported by the library.

    Not a complete list. Open an issue for any gateway not represented here.

    Attributes:
        MHServer:
        MH200:
        F452:
        F452V:
        MHServer2:
        H4684:
        MH202:
    """

    GENERIC = "0"
    MHServer = "2"
    MH200 = "4"
    F452 = "6"
    F452V = "7"
    MHServer2 = "11"
    H4684 = "12"
    HL4684 = "23"
    MH202 = "200"

    @classmethod
    def _missing_(cls, value):
        log.warning("The gateway model %s was not found in the known models.", value)
        log.warning("Please, open an issue on GitHub, attach the logs and the model name.")
        return GatewayModel.GENERIC


class WhatGateway(What, StrEnum):
    """Dimension tags for gateway queries and events.

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

    TIME = "0"
    DATE = "1"
    IP_ADDRESS = "10"
    NET_MASK = "11"
    MAC_ADDRESS = "12"
    DEVICE_TYPE = "15"
    FIRMWARE_VERSION = "16"
    UPTIME = "19"
    DATE_TIME = "22"
    KERNEL_VERSION = "23"
    DISTRIBUTION_VERSION = "24"


@item(Who.GATEWAY)
class Gateway(BaseItem):
    """Gateway item — exposes gateway/bus metadata and clock."""

    def __init__(self, client: BaseClient, where: Where | str = ""):
        """Initializes the item.

        Args:
            client: The client to use to communicate with the server.
        """
        super().__init__(client, Where(""))

    @staticmethod
    def _parse_own_timezone(t: Value) -> datetime.timezone:
        if t.string == "":
            return datetime.timezone.utc

        sign = t.string[0]
        hours = int(t.string[1:3])

        return datetime.timezone(
            datetime.timedelta(hours=hours) if sign == "0" else -datetime.timedelta(hours=hours)
        )

    @staticmethod
    def _tz_to_own_tz(tzinfo: datetime.tzinfo | None) -> Value:
        if tzinfo is None:
            raise ValueError("The timezone must be set in the datetime object.")

        tz = tzinfo.utcoffset(None)
        if tz is None:
            raise ValueError("The timezone must be set in the datetime object.")

        sign = "0" if tz >= datetime.timedelta(0) else "1"  # type: ignore[union-attr]
        hours = abs(tz.seconds) // 3600  # type: ignore[union-attr]

        t = Value(f"{sign}{hours:03d}")
        return t

    # ------------------------------------------------------------------
    # Sync decoders: take a message, return a typed value. No I/O.
    # Used by both the public `get_*` methods and the event parser.
    # ------------------------------------------------------------------

    @classmethod
    def _decode_time(cls, message: DimensionResponse | DimensionWriting) -> datetime.time:
        h_v, m_v, s_v, t_v = message.values
        return datetime.time(
            int(h_v.string), int(m_v.string), int(s_v.string),
            tzinfo=cls._parse_own_timezone(t_v),
        )

    @staticmethod
    def _decode_date(message: DimensionResponse | DimensionWriting) -> datetime.date:
        _w, d, m, a = message.values
        return datetime.date(int(a.string), int(m.string), int(d.string))

    @staticmethod
    def _decode_ip(message: DimensionResponse | DimensionWriting) -> ipaddress.IPv4Address:
        o1, o2, o3, o4 = message.values
        return ipaddress.IPv4Address(
            f"{int(o1.string)}.{int(o2.string)}.{int(o3.string)}.{int(o4.string)}"
        )

    @staticmethod
    def _decode_netmask(message: DimensionResponse | DimensionWriting) -> str:
        o1, o2, o3, o4 = message.values
        return f"{int(o1.string)}.{int(o2.string)}.{int(o3.string)}.{int(o4.string)}"

    @staticmethod
    def _decode_macaddress(message: DimensionResponse | DimensionWriting) -> str:
        o1, o2, o3, o4, o5, o6 = message.values
        return f"{o1.string}:{o2.string}:{o3.string}:{o4.string}:{o5.string}:{o6.string}"

    @staticmethod
    def _decode_model(message: DimensionResponse | DimensionWriting) -> GatewayModel:
        return GatewayModel(message.values[0].string)

    @staticmethod
    def _decode_version_triplet(message: DimensionResponse | DimensionWriting) -> str:
        v = message.values[0].string
        r = message.values[1].string
        b = message.values[2].string
        return f"{v}.{r}.{b}"

    @staticmethod
    def _decode_uptime(message: DimensionResponse | DimensionWriting) -> datetime.timedelta:
        d = int(message.values[0].string)
        h = int(message.values[1].string)
        m = int(message.values[2].string)
        s = int(message.values[3].string)
        return datetime.timedelta(days=d, hours=h, minutes=m, seconds=s)

    @classmethod
    def _decode_datetime(
        cls, message: DimensionResponse | DimensionWriting
    ) -> datetime.datetime:
        h = int(message.values[0].string)
        m = int(message.values[1].string)
        s = int(message.values[2].string)
        t = message.values[3]
        # message.values[4] is the day-of-week, ignored here.
        d = int(message.values[5].string)
        mo = int(message.values[6].string)
        y = int(message.values[7].string)
        return datetime.datetime(y, mo, d, h, m, s, tzinfo=cls._parse_own_timezone(t))

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def get_time(self, *, message: EventMessage = None) -> datetime.time:
        """Requests the time of the gateway and bus."""
        msg = message if message is not None else await self._single_dim_req(WhatGateway.TIME)
        return self._decode_time(msg)

    async def set_time(self, bus_time: datetime.time):
        """Sets the time of the gateway and bus.

        Args:
            bus_time: the time to set with the timezone.

        Raises:
            ValueError: if bus_time.tzinfo is None or bus_time.tzinfo.utcoffset(None) is None.
        """
        t = self._tz_to_own_tz(bus_time.tzinfo)
        h = Value(f"{bus_time.hour:02d}")
        m = Value(f"{bus_time.minute:02d}")
        s = Value(f"{bus_time.second:02d}")
        await self.send_dimension_writing(WhatGateway.TIME, h, m, s, t)

    async def get_date(self, *, message: EventMessage = None) -> datetime.date:
        """Requests the date of the gateway and bus."""
        msg = message if message is not None else await self._single_dim_req(WhatGateway.DATE)
        return self._decode_date(msg)

    async def set_date(self, bus_date: datetime.date):
        """Sets the date of the gateway and bus."""
        d = Value(f"{bus_date.day:02d}")
        m = Value(f"{bus_date.month:02d}")
        a = Value(f"{bus_date.year}")
        if bus_date.weekday() == 6:
            w = Value("00")
        else:
            w = Value(f"{bus_date.weekday() + 1:02d}")
        await self.send_dimension_writing(WhatGateway.DATE, w, d, m, a)

    async def get_ip(self, *, message: EventMessage = None) -> ipaddress.IPv4Address:
        """Requests the IP address of the gateway."""
        msg = message if message is not None else await self._single_dim_req(WhatGateway.IP_ADDRESS)
        return self._decode_ip(msg)

    async def get_netmask(self, *, message: EventMessage = None) -> str:
        """Requests the net mask of the gateway."""
        msg = message if message is not None else await self._single_dim_req(WhatGateway.NET_MASK)
        return self._decode_netmask(msg)

    async def get_macaddress(self, *, message: EventMessage = None) -> str:
        """Requests the MAC address of the gateway."""
        msg = (
            message
            if message is not None
            else await self._single_dim_req(WhatGateway.MAC_ADDRESS)
        )
        return self._decode_macaddress(msg)

    async def get_netinfo(self) -> ipaddress.IPv4Network:
        """Combines the net mask and the IP address to get the network info."""
        ip = await self.get_ip()
        netmask = await self.get_netmask()
        return ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)

    async def get_model(self, *, message: EventMessage = None) -> GatewayModel:
        """Requests the device type of the gateway."""
        msg = (
            message
            if message is not None
            else await self._single_dim_req(WhatGateway.DEVICE_TYPE)
        )
        return self._decode_model(msg)

    async def get_firmware(self, *, message: EventMessage = None) -> str:
        """Requests the firmware version of the gateway."""
        msg = (
            message
            if message is not None
            else await self._single_dim_req(WhatGateway.FIRMWARE_VERSION)
        )
        return self._decode_version_triplet(msg)

    async def get_uptime(self, *, message: EventMessage = None) -> datetime.timedelta:
        """Requests the uptime of the gateway."""
        msg = message if message is not None else await self._single_dim_req(WhatGateway.UPTIME)
        return self._decode_uptime(msg)

    async def get_datetime(self, *, message: EventMessage = None) -> datetime.datetime:
        """Requests the date and time of the gateway."""
        msg = message if message is not None else await self._single_dim_req(WhatGateway.DATE_TIME)
        return self._decode_datetime(msg)

    async def set_datetime(self, bus_time: datetime.datetime):
        """Sets the date and time of the gateway.

        Args:
            bus_time: the date and time to set with the timezone.

        Raises:
            ValueError: if bus_time.tzinfo is None or bus_time.tzinfo.utcoffset(None) is None.
        """
        t = self._tz_to_own_tz(bus_time.tzinfo)
        h = Value(f"{bus_time.hour:02d}")
        m = Value(f"{bus_time.minute:02d}")
        s = Value(f"{bus_time.second:02d}")

        d = Value(f"{bus_time.day:02d}")
        mo = Value(f"{bus_time.month:02d}")
        y = Value(f"{bus_time.year}")

        await self.send_dimension_writing(WhatGateway.DATE_TIME, h, m, s, t, d, mo, y)

    async def get_kernel_version(self, *, message: EventMessage = None) -> str:
        """Requests the linux kernel version of the gateway."""
        msg = (
            message
            if message is not None
            else await self._single_dim_req(WhatGateway.KERNEL_VERSION)
        )
        return self._decode_version_triplet(msg)

    async def get_distribution_version(self, *, message: EventMessage = None) -> str:
        """Requests the os distribution version of the gateway."""
        msg = (
            message
            if message is not None
            else await self._single_dim_req(WhatGateway.DISTRIBUTION_VERSION)
        )
        return self._decode_version_triplet(msg)
