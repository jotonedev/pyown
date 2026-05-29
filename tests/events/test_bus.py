"""Behavioural tests for `EventBus`, `Subscription`, and dispatch semantics."""

import asyncio
import logging
import unittest
from dataclasses import dataclass
from unittest.mock import MagicMock

from pyown.events import Event, EventBus
from pyown.items.base import BaseItem
from pyown.tags import Where


@dataclass(frozen=True, slots=True)
class SampleEvent(Event):
    value: int


@dataclass(frozen=True, slots=True)
class OtherEvent(Event):
    label: str


def _item() -> BaseItem:
    return MagicMock(spec=BaseItem)


class EventBusTests(unittest.IsolatedAsyncioTestCase):
    async def test_subscribe_dispatch_round_trip(self):
        bus = EventBus()
        seen: list[SampleEvent] = []

        async def handler(event: SampleEvent):
            seen.append(event)

        bus.subscribe(SampleEvent, handler)
        event = SampleEvent(_item(), Where("11"), value=42)
        await bus.dispatch(event)

        self.assertEqual(seen, [event])

    async def test_subscribe_all_receives_everything(self):
        bus = EventBus()
        seen: list[Event] = []

        async def handler(event: Event):
            seen.append(event)

        bus.subscribe_all(handler)

        e1 = SampleEvent(_item(), Where("11"), value=1)
        e2 = OtherEvent(_item(), Where("21"), label="x")
        await bus.dispatch(e1)
        await bus.dispatch(e2)

        self.assertEqual(seen, [e1, e2])

    async def test_subscribe_to_base_event_is_catch_all(self):
        bus = EventBus()
        seen: list[Event] = []

        async def handler(event: Event):
            seen.append(event)

        bus.subscribe(Event, handler)
        e1 = SampleEvent(_item(), Where("11"), value=1)
        e2 = OtherEvent(_item(), Where("21"), label="x")
        await bus.dispatch(e1)
        await bus.dispatch(e2)

        self.assertEqual(seen, [e1, e2])

    async def test_where_filter_match(self):
        bus = EventBus()
        seen: list[SampleEvent] = []

        async def handler(event: SampleEvent):
            seen.append(event)

        bus.subscribe(SampleEvent, handler, where="11")

        await bus.dispatch(SampleEvent(_item(), Where("11"), value=1))
        await bus.dispatch(SampleEvent(_item(), Where("12"), value=2))

        self.assertEqual([e.value for e in seen], [1])

    async def test_where_filter_accepts_where_object(self):
        bus = EventBus()
        seen: list[SampleEvent] = []

        async def handler(event: SampleEvent):
            seen.append(event)

        bus.subscribe(SampleEvent, handler, where=Where("11"))

        await bus.dispatch(SampleEvent(_item(), Where("11"), value=1))
        await bus.dispatch(SampleEvent(_item(), Where("12"), value=2))

        self.assertEqual([e.value for e in seen], [1])

    async def test_unsubscribe_stops_delivery(self):
        bus = EventBus()
        calls = 0

        async def handler(event: SampleEvent):
            nonlocal calls
            calls += 1

        sub = bus.subscribe(SampleEvent, handler)
        await bus.dispatch(SampleEvent(_item(), Where("11"), value=1))
        sub.unsubscribe()
        await bus.dispatch(SampleEvent(_item(), Where("11"), value=2))
        self.assertEqual(calls, 1)

    async def test_unsubscribe_subscribe_all(self):
        bus = EventBus()
        calls = 0

        async def handler(event: Event):
            nonlocal calls
            calls += 1

        sub = bus.subscribe_all(handler)
        await bus.dispatch(SampleEvent(_item(), Where("11"), value=1))
        sub.unsubscribe()
        await bus.dispatch(SampleEvent(_item(), Where("11"), value=2))
        self.assertEqual(calls, 1)

    async def test_subscription_context_manager(self):
        bus = EventBus()
        calls = 0

        async def handler(event: SampleEvent):
            nonlocal calls
            calls += 1

        with bus.subscribe(SampleEvent, handler):
            await bus.dispatch(SampleEvent(_item(), Where("11"), value=1))
        await bus.dispatch(SampleEvent(_item(), Where("11"), value=2))
        self.assertEqual(calls, 1)

    async def test_handler_exception_isolated(self):
        bus = EventBus()
        calls = 0

        async def boom(event: SampleEvent):
            raise RuntimeError("kaboom")

        async def survivor(event: SampleEvent):
            nonlocal calls
            calls += 1

        bus.subscribe(SampleEvent, boom)
        bus.subscribe(SampleEvent, survivor)
        with self.assertLogs("pyown.events.bus", level=logging.ERROR):
            await bus.dispatch(SampleEvent(_item(), Where("11"), value=1))
        self.assertEqual(calls, 1)

    async def test_dispatch_with_no_handlers_is_noop(self):
        bus = EventBus()
        await bus.dispatch(SampleEvent(_item(), Where("11"), value=1))

    async def test_multiple_subscribers_all_fire(self):
        bus = EventBus()
        a, b = 0, 0

        async def ha(e):
            nonlocal a
            a += 1

        async def hb(e):
            nonlocal b
            b += 1

        bus.subscribe(SampleEvent, ha)
        bus.subscribe(SampleEvent, hb)
        await bus.dispatch(SampleEvent(_item(), Where("11"), value=1))
        self.assertEqual((a, b), (1, 1))

    async def test_concurrent_dispatches_independent(self):
        bus = EventBus()
        seen: list[int] = []
        gate = asyncio.Event()

        async def handler(event: SampleEvent):
            await gate.wait()
            seen.append(event.value)

        bus.subscribe(SampleEvent, handler)

        t1 = asyncio.create_task(bus.dispatch(SampleEvent(_item(), Where("11"), value=1)))
        t2 = asyncio.create_task(bus.dispatch(SampleEvent(_item(), Where("11"), value=2)))
        await asyncio.sleep(0)
        gate.set()
        await asyncio.gather(t1, t2)
        self.assertCountEqual(seen, [1, 2])
