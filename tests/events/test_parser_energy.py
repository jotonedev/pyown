"""Parser tests for energy management (WHO=18). Payloads from docs/original/who18.md."""

import unittest
from datetime import datetime

from pyown.items.energy import (
    EnergyActivePowerEvent,
    EnergyActuatorsInfoEvent,
    EnergyDailyTotalizersHourlyEvent,
    EnergyDifferentialCurrentLevelEvent,
    EnergyMonthlyAverageHourlyEvent,
    EnergyMonthlyTotalizersCurrentYearEvent,
    EnergyMonthlyTotalizersLastYearEvent,
    EnergyPartialTotalizerCurrentDayEvent,
    EnergyPartialTotalizerCurrentMonthEvent,
    EnergyStopGoStatusEvent,
    EnergyTotalizerEvent,
    EnergyUnitPerMonthEvent,
    EnergyUnitTotalizerEvent,
)
from pyown.tags import Who

from ._helpers import make_item, parse_one_own


class EnergyParserTests(unittest.TestCase):
    def setUp(self):
        # 51 = power meter where; valid per the EnergyManagement.get_type rule.
        self.power = make_item(Who.ENERGY_MANAGEMENT, "51")
        self.stop_go = make_item(Who.ENERGY_MANAGEMENT, "11")

    def test_active_power(self):
        event = parse_one_own(self.power, "*#18*51*113*1234##")
        self.assertEqual(event, EnergyActivePowerEvent(self.power, self.power.where, power=1234.0))

    def test_energy_unit_totalizer(self):
        event = parse_one_own(self.power, "*#18*51*51*5000##")
        self.assertEqual(event, EnergyUnitTotalizerEvent(self.power, self.power.where, energy=5000.0))

    def test_energy_unit_per_month(self):
        # Dimension with two parameters: 52#YY#MM → year, month.
        event = parse_one_own(self.power, "*#18*51*52#26#3*123##")
        self.assertEqual(
            event,
            EnergyUnitPerMonthEvent(self.power, self.power.where, month=3, year=26, energy=123.0),
        )

    def test_partial_totalizer_current_month(self):
        event = parse_one_own(self.power, "*#18*51*53*42##")
        self.assertEqual(event,
            EnergyPartialTotalizerCurrentMonthEvent(self.power, self.power.where, energy=42.0))

    def test_partial_totalizer_current_day(self):
        event = parse_one_own(self.power, "*#18*51*54*7##")
        self.assertEqual(event,
            EnergyPartialTotalizerCurrentDayEvent(self.power, self.power.where, energy=7.0))

    def test_actuators_info(self):
        # ActuatorStatus: 6 positions in a string.
        # Last digit encodes advanced/basic: '1' → advanced=True, anything else → False.
        # disabled=1, forcing=0, threshold=1, protection=0, phase=1, advanced-byte='1'
        event = parse_one_own(self.power, "*#18*51*71*101011##")
        self.assertIsInstance(event, EnergyActuatorsInfoEvent)
        self.assertTrue(event.status.disabled)
        self.assertFalse(event.status.forcing)
        self.assertTrue(event.status.threshold)
        self.assertFalse(event.status.protection)
        self.assertTrue(event.status.phase)
        self.assertTrue(event.status.advanced)

    def test_actuators_info_basic_mode(self):
        # advanced-byte='2' → advanced=False
        event = parse_one_own(self.power, "*#18*51*71*000002##")
        self.assertFalse(event.status.advanced)

    def test_totalizer_since_reset(self):
        # 72#1 → totalizer #1; values: energy, d, m, y, h, mi
        event = parse_one_own(self.power, "*#18*51*72#1*9999*15*03*2026*14*30##")
        self.assertEqual(
            event,
            EnergyTotalizerEvent(
                self.power, self.power.where,
                totalizer=1,
                last_reset=datetime(2026, 3, 15, 14, 30),
                energy=9999.0,
            ),
        )

    def test_differential_current_level(self):
        event = parse_one_own(self.power, "*#18*51*73*2##")
        self.assertEqual(event,
            EnergyDifferentialCurrentLevelEvent(self.power, self.power.where, level=2))

    def test_stop_go_general(self):
        # 13-char bitfield. Make every bit '1' except positions 2 and 5.
        bits = "1011101111111"
        event = parse_one_own(self.stop_go, f"*#18*11*250*{bits}##")
        self.assertIsInstance(event, EnergyStopGoStatusEvent)
        s = event.status
        self.assertTrue(s.open)
        self.assertFalse(s.failure)
        self.assertTrue(s.block)
        self.assertTrue(s.open_cc)
        self.assertTrue(s.open_ground_fault)
        self.assertFalse(s.open_vmax)
        self.assertTrue(s.self_test_off)

    def test_daily_totalizers_hourly(self):
        event = parse_one_own(self.power, "*#18*51*511#3*14*250##")
        self.assertEqual(
            event,
            EnergyDailyTotalizersHourlyEvent(
                self.power, self.power.where, month=3, hour=14, energy=250.0
            ),
        )

    def test_monthly_average_hourly(self):
        event = parse_one_own(self.power, "*#18*51*512#5*22*180##")
        self.assertEqual(
            event,
            EnergyMonthlyAverageHourlyEvent(
                self.power, self.power.where, month=5, hour=22, energy=180.0
            ),
        )

    def test_monthly_totalizers_current_year(self):
        event = parse_one_own(self.power, "*#18*51*513#7*15*420##")
        self.assertEqual(
            event,
            EnergyMonthlyTotalizersCurrentYearEvent(
                self.power, self.power.where, month=7, day=15, energy=420.0
            ),
        )

    def test_monthly_totalizers_last_year(self):
        event = parse_one_own(self.power, "*#18*51*514#7*15*399##")
        self.assertEqual(
            event,
            EnergyMonthlyTotalizersLastYearEvent(
                self.power, self.power.where, month=7, day=15, energy=399.0
            ),
        )

    def test_unhandled_dimension(self):
        from pyown.events.registry import get_parser
        from pyown.messages import parse_message

        msg = parse_message("*#18*51*99*1##")
        self.assertEqual(list(get_parser(Who.ENERGY_MANAGEMENT)(self.power, msg)), [])
