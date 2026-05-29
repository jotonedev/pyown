"""Parser tests for cameras / video door entry (WHO=7)."""

import unittest

from pyown.items.camera import CameraStatusEvent, WhatCamera
from pyown.tags import Where, Who

from ._helpers import make_item, parse_one_own


class CameraParserTests(unittest.TestCase):
    def setUp(self):
        self.item = make_item(Who.VIDEO_DOOR_ENTRY, "4000")

    def test_receive_video(self):
        event = parse_one_own(self.item, "*7*0*4000##")
        self.assertIsInstance(event, CameraStatusEvent)
        self.assertEqual(event.where, Where("4000"))
        self.assertEqual(event.command, WhatCamera.RECEIVE_VIDEO)

    def test_free_resources(self):
        # The protocol allows free_resources with a WHERE too; the parser only
        # fires when a NormalMessage carries a WHERE (parse_message requires it
        # for the NORMAL framing). Test with WHERE form.
        event = parse_one_own(self.item, "*7*9*4000##")
        self.assertEqual(event.command, WhatCamera.FREE_RESOURCES)
