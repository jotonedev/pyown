import asyncio
import unittest

# ruff: noqa: F401
from unittest.mock import MagicMock

from pyown.exceptions import ParseError
from pyown.messages import ACK
from pyown.protocol.protocol import OWNProtocol


class OWNProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.on_connection_start = asyncio.Future()
        self.on_connection_end = asyncio.Future()

        self.protocol = OWNProtocol(self.on_connection_start, self.on_connection_end)

    async def test_connection_made(self):
        transport = unittest.mock.MagicMock()
        self.protocol.connection_made(transport)
        self.assertEqual(self.on_connection_start.result(), transport)

    async def test_connection_lost(self):
        exc = Exception()
        self.protocol.connection_lost(exc)
        self.assertEqual(self.on_connection_end.exception(), exc)

    async def test_connection_lost_no_exception(self):
        self.protocol.connection_lost(None)
        self.assertIsNone(self.on_connection_end.result())

    async def test_data_received(self):
        data = b"*#*1##"  # ACK message

        self.protocol.data_received(data)
        message = await self.protocol._messages_queue.get()
        self.assertIsInstance(message, ACK)
        self.assertEqual(message.bytes, data)

    async def test_data_received_invalid(self):
        data = b"deadbeef"

        with self.assertRaises(ParseError):
            self.protocol.data_received(data)

    async def test_data_received_not_ascii(self):
        data = b"\xff\xff\xff"

        with self.assertRaises(UnicodeDecodeError):
            self.protocol.data_received(data)
