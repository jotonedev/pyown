"""End-to-end test: inject a frame into the protocol queue and verify the
typed event reaches a subscribed handler via `Client.loop()`."""

import asyncio
import unittest
from unittest.mock import MagicMock

from pyown.client import Client, SessionType
from pyown.items.automation import AutomationStatusEvent, WhatAutomation
from pyown.items.lighting import LightStatusEvent
from pyown.messages import parse_message
from pyown.protocol import OWNProtocol


class ClientDispatchTests(unittest.IsolatedAsyncioTestCase):
    async def _wire_client(self):
        """Build a Client wired to a fake protocol whose `receive_messages`
        pops from an in-memory queue."""
        client = Client("test", 0, "test", session_type=SessionType.EventSession)

        # Stand up a real protocol object so its message queue is real.
        protocol = OWNProtocol(
            on_connection_start=asyncio.Future(),
            on_connection_end=asyncio.Future(),
        )

        transport = MagicMock()
        transport.is_closing = MagicMock(side_effect=[False, True])
        client._transport = transport
        client._protocol = protocol

        return client, protocol

    async def test_light_status_round_trip(self):
        client, protocol = await self._wire_client()

        seen: list[LightStatusEvent] = []

        async def handler(event: LightStatusEvent):
            seen.append(event)

        client.events.subscribe(LightStatusEvent, handler)

        await protocol._messages_queue.put(parse_message("*1*1*11##"))

        await client.loop()

        # Wait for the dispatched task to complete.
        pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)

        self.assertEqual(len(seen), 1)
        self.assertTrue(seen[0].on)
        self.assertEqual(str(seen[0].where), "11")

    async def test_where_filter_in_pipeline(self):
        client, protocol = await self._wire_client()
        transport = client._transport
        transport.is_closing = MagicMock(side_effect=[False, False, True])

        match: list[LightStatusEvent] = []
        miss: list[LightStatusEvent] = []

        async def m(event: LightStatusEvent):
            match.append(event)

        async def n(event: LightStatusEvent):
            miss.append(event)

        client.events.subscribe(LightStatusEvent, m, where="11")
        client.events.subscribe(LightStatusEvent, n, where="12")

        await protocol._messages_queue.put(parse_message("*1*1*11##"))
        await protocol._messages_queue.put(parse_message("*1*0*11##"))

        await client.loop()
        pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)

        self.assertEqual(len(match), 2)
        self.assertEqual(len(miss), 0)

    async def test_automation_dispatch(self):
        client, protocol = await self._wire_client()

        seen: list[AutomationStatusEvent] = []

        async def handler(event: AutomationStatusEvent):
            seen.append(event)

        client.events.subscribe(AutomationStatusEvent, handler)

        await protocol._messages_queue.put(parse_message("*2*1*32##"))

        await client.loop()
        pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)

        self.assertEqual(len(seen), 1)
        self.assertEqual(seen[0].state, WhatAutomation.UP)

    async def test_subscribe_all_in_pipeline(self):
        client, protocol = await self._wire_client()
        transport = client._transport
        transport.is_closing = MagicMock(side_effect=[False, False, True])

        seen = []

        async def all_handler(event):
            seen.append(type(event).__name__)

        client.events.subscribe_all(all_handler)

        await protocol._messages_queue.put(parse_message("*1*1*11##"))
        await protocol._messages_queue.put(parse_message("*2*1*32##"))

        await client.loop()
        pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)

        self.assertEqual(seen, ["LightStatusEvent", "AutomationStatusEvent"])
