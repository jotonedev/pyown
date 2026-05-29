"""Parser tests for lighting (WHO=1). Payloads from docs/original/who1.md."""

import unittest

from pyown.items.lighting import (
    LightHSVEvent,
    LightLuminosityEvent,
    LightStatusEvent,
    LightTemporizationEvent,
    LightWhiteTempEvent,
)
from pyown.tags import Who, Where

from ._helpers import make_item, parse_one_own


class LightingParserTests(unittest.TestCase):
    def setUp(self):
        self.item = make_item(Who.LIGHTING, "11")

    def test_status_on(self):
        # *1*1*11##  → light at 11 turns ON
        event = parse_one_own(self.item, "*1*1*11##")
        self.assertIsInstance(event, LightStatusEvent)
        self.assertEqual(event.where, Where("11"))
        self.assertTrue(event.on)

    def test_status_off(self):
        event = parse_one_own(self.item, "*1*0*11##")
        self.assertIsInstance(event, LightStatusEvent)
        self.assertFalse(event.on)

    def test_luminosity_dim_1(self):
        # *#1*11*1*150*100## → dimmer brightness=150, speed=100
        event = parse_one_own(self.item, "*#1*11*1*150*100##")
        self.assertEqual(
            event, LightLuminosityEvent(self.item, Where("11"), luminosity=150, speed=100)
        )

    def test_temporization_dim_2(self):
        # *#1*11*2*1*30*45##
        event = parse_one_own(self.item, "*#1*11*2*1*30*45##")
        self.assertEqual(
            event,
            LightTemporizationEvent(self.item, Where("11"), hour=1, minute=30, second=45),
        )

    def test_luminosity_dim_8(self):
        event = parse_one_own(self.item, "*#1*11*8*200*50##")
        self.assertEqual(
            event, LightLuminosityEvent(self.item, Where("11"), luminosity=200, speed=50)
        )

    def test_hsv_dim_12(self):
        event = parse_one_own(self.item, "*#1*11*12*180*50*75##")
        self.assertEqual(
            event,
            LightHSVEvent(self.item, Where("11"), hue=180, saturation=50, value=75),
        )

    def test_white_temp_dim_13(self):
        event = parse_one_own(self.item, "*#1*11*13*4000##")
        self.assertEqual(
            event, LightWhiteTempEvent(self.item, Where("11"), temperature=4000)
        )

    def test_unhandled_dimension_yields_nothing(self):
        from pyown.events.registry import get_parser
        from pyown.messages import parse_message

        msg = parse_message("*#1*11*99*1##")
        events = list(get_parser(Who.LIGHTING)(self.item, msg))
        self.assertEqual(events, [])
