"""Parser tests for automation (WHO=2). Payloads from docs/original/who2.md."""

import unittest

from pyown.items.automation import AutomationStatusEvent, WhatAutomation
from pyown.tags import Where, Who

from ._helpers import make_item, parse_one_own


class AutomationParserTests(unittest.TestCase):
    def setUp(self):
        self.item = make_item(Who.AUTOMATION, "32")

    def test_stop(self):
        event = parse_one_own(self.item, "*2*0*32##")
        self.assertEqual(
            event, AutomationStatusEvent(self.item, Where("32"), state=WhatAutomation.STOP)
        )

    def test_up(self):
        event = parse_one_own(self.item, "*2*1*32##")
        self.assertEqual(event.state, WhatAutomation.UP)

    def test_down(self):
        event = parse_one_own(self.item, "*2*2*32##")
        self.assertEqual(event.state, WhatAutomation.DOWN)
