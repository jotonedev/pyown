"""Tests for the parser/item registry and `bootstrap()`."""

import unittest
from dataclasses import dataclass
from unittest.mock import MagicMock

from pyown.client import BaseClient
from pyown.events import (
    Event,
    all_whos,
    bootstrap,
    get_item_type,
    get_parser,
    item,
    parser,
)
from pyown.events.registry import _item_types, _parsers
from pyown.items.base import BaseItem
from pyown.items.lighting.events import parse_lighting
from pyown.tags import Who


class RegistryTests(unittest.TestCase):
    def test_bootstrap_registers_all_known_whos(self):
        bootstrap()
        expected = {
            Who.LIGHTING,
            Who.AUTOMATION,
            Who.GATEWAY,
            Who.ENERGY_MANAGEMENT,
            Who.VIDEO_DOOR_ENTRY,
        }
        registered_items = set(_item_types.keys())
        registered_parsers = set(_parsers.keys())
        self.assertTrue(expected <= registered_items, f"missing items: {expected - registered_items}")
        self.assertTrue(expected <= registered_parsers, f"missing parsers: {expected - registered_parsers}")

    def test_bootstrap_idempotent(self):
        bootstrap()
        snap = (dict(_item_types), dict(_parsers))
        bootstrap()
        self.assertEqual(snap[0], _item_types)
        self.assertEqual(snap[1], _parsers)

    def test_all_whos_intersection(self):
        bootstrap()
        for who in {
            Who.LIGHTING, Who.AUTOMATION, Who.GATEWAY,
            Who.ENERGY_MANAGEMENT, Who.VIDEO_DOOR_ENTRY,
        }:
            self.assertIn(who, all_whos())

    def test_get_parser_and_item_known(self):
        bootstrap()
        self.assertIs(get_parser(Who.LIGHTING), parse_lighting)
        light_cls = get_item_type(Who.LIGHTING)
        self.assertIsNotNone(light_cls)
        # Concrete `Light` registered, not `BaseLight`.
        self.assertEqual(light_cls.__name__, "Light")

    def test_get_parser_unknown_returns_none(self):
        bootstrap()
        # SCENE (WHO=0) has no item or parser registered.
        self.assertIsNone(get_parser(Who.SCENE))
        self.assertIsNone(get_item_type(Who.SCENE))

    def test_duplicate_parser_registration_raises(self):
        bootstrap()
        with self.assertRaises(RuntimeError):
            @parser(Who.LIGHTING)
            def shadow_parser(item: BaseItem, message):
                yield from ()

    def test_duplicate_item_registration_raises(self):
        bootstrap()
        with self.assertRaises(RuntimeError):
            @item(Who.LIGHTING)
            class Shadow(BaseItem):
                pass

    def test_item_decorator_sets_who(self):
        bootstrap()
        cls = get_item_type(Who.GATEWAY)
        self.assertEqual(cls._who, Who.GATEWAY)


class ItemInstantiationTests(unittest.TestCase):
    def test_instantiate_each_item_type(self):
        bootstrap()
        client = MagicMock(spec=BaseClient)
        # WHERE values valid for each item, derived from docs/original.
        cases = {
            Who.LIGHTING: "11",
            Who.AUTOMATION: "32",
            Who.GATEWAY: "",
            Who.ENERGY_MANAGEMENT: "51",   # power meter
            Who.VIDEO_DOOR_ENTRY: "4000",
        }
        for who, where in cases.items():
            cls = get_item_type(who)
            self.assertIsNotNone(cls, f"No class for {who}")
            inst = cls(client, where)
            self.assertEqual(inst._who, who)
