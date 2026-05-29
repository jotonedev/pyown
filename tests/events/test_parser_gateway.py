"""Parser tests for gateway (WHO=13). Payloads modelled on docs/original/who13.md."""

import datetime
import ipaddress
import unittest

from pyown.items.gateway import (
    Gateway,
    GatewayDateEvent,
    GatewayDateTimeEvent,
    GatewayDistributionVersionEvent,
    GatewayFirmwareEvent,
    GatewayIPEvent,
    GatewayKernelVersionEvent,
    GatewayMacAddressEvent,
    GatewayModel,
    GatewayModelEvent,
    GatewayNetmaskEvent,
    GatewayTimeEvent,
    GatewayUptimeEvent,
)
from pyown.tags import Value, Who

from ._helpers import make_item, parse_one_own


class GatewayParserTests(unittest.TestCase):
    def setUp(self):
        self.item = make_item(Who.GATEWAY, "")

    def test_time_utc(self):
        event = parse_one_own(self.item, "*#13**0*14*30*45*000##")
        self.assertIsInstance(event, GatewayTimeEvent)
        self.assertEqual(event.time, datetime.time(14, 30, 45, tzinfo=datetime.timezone.utc))

    def test_time_positive_offset(self):
        # sign=0, offset=002 hours
        event = parse_one_own(self.item, "*#13**0*14*30*45*002##")
        self.assertEqual(
            event.time,
            datetime.time(14, 30, 45, tzinfo=datetime.timezone(datetime.timedelta(hours=2))),
        )

    def test_time_negative_offset(self):
        # sign=1, offset=005 hours → -5h
        event = parse_one_own(self.item, "*#13**0*14*30*45*105##")
        self.assertEqual(
            event.time,
            datetime.time(14, 30, 45, tzinfo=datetime.timezone(datetime.timedelta(hours=-5))),
        )

    def test_date(self):
        # day-of-week, day, month, year (year zero-padded raw string)
        event = parse_one_own(self.item, "*#13**1*02*15*03*2026##")
        self.assertIsInstance(event, GatewayDateEvent)
        self.assertEqual(event.date, datetime.date(2026, 3, 15))

    def test_ip(self):
        event = parse_one_own(self.item, "*#13**10*192*168*1*35##")
        self.assertEqual(event, GatewayIPEvent(self.item, self.item.where,
                                               ip=ipaddress.IPv4Address("192.168.1.35")))

    def test_netmask(self):
        event = parse_one_own(self.item, "*#13**11*255*255*255*0##")
        self.assertEqual(event, GatewayNetmaskEvent(self.item, self.item.where, netmask="255.255.255.0"))

    def test_mac_address(self):
        event = parse_one_own(self.item, "*#13**12*001*002*003*004*005*006##")
        self.assertEqual(event.mac, "001:002:003:004:005:006")

    def test_model(self):
        event = parse_one_own(self.item, "*#13**15*200##")
        self.assertEqual(event, GatewayModelEvent(self.item, self.item.where, model=GatewayModel.MH202))

    def test_firmware(self):
        event = parse_one_own(self.item, "*#13**16*1*2*3##")
        self.assertEqual(event, GatewayFirmwareEvent(self.item, self.item.where, version="1.2.3"))

    def test_uptime(self):
        event = parse_one_own(self.item, "*#13**19*1*02*03*04##")
        self.assertEqual(
            event.uptime, datetime.timedelta(days=1, hours=2, minutes=3, seconds=4)
        )

    def test_kernel_version(self):
        event = parse_one_own(self.item, "*#13**23*5*15*100##")
        self.assertEqual(event, GatewayKernelVersionEvent(self.item, self.item.where, version="5.15.100"))

    def test_distribution_version(self):
        event = parse_one_own(self.item, "*#13**24*22*04*1##")
        self.assertEqual(
            event,
            GatewayDistributionVersionEvent(self.item, self.item.where, version="22.04.1"),
        )

    def test_datetime(self):
        # h, m, s, tz, dow, day, mo, year
        event = parse_one_own(self.item, "*#13**22*14*30*45*000*0*15*03*2026##")
        self.assertIsInstance(event, GatewayDateTimeEvent)
        self.assertEqual(
            event.datetime,
            datetime.datetime(2026, 3, 15, 14, 30, 45, tzinfo=datetime.timezone.utc),
        )

    def test_unhandled_dimension(self):
        from pyown.events.registry import get_parser
        from pyown.messages import parse_message

        msg = parse_message("*#13**99*1##")
        self.assertEqual(list(get_parser(Who.GATEWAY)(self.item, msg)), [])


class TimezoneHelperTests(unittest.TestCase):
    """Direct tests for the timezone parsing quirks."""

    def test_empty_string_is_utc(self):
        self.assertEqual(Gateway._parse_own_timezone(Value("")), datetime.timezone.utc)

    def test_positive_offset(self):
        self.assertEqual(
            Gateway._parse_own_timezone(Value("003")),
            datetime.timezone(datetime.timedelta(hours=3)),
        )

    def test_negative_offset(self):
        self.assertEqual(
            Gateway._parse_own_timezone(Value("108")),
            datetime.timezone(datetime.timedelta(hours=-8)),
        )
