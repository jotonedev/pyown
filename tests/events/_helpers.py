"""Shared helpers for event-related tests."""

from unittest.mock import MagicMock

from pyown.client import BaseClient
from pyown.events import Event, bootstrap, get_item_type, get_parser
from pyown.items.base import BaseItem
from pyown.messages import BaseMessage, parse_message
from pyown.tags import Who


def fake_client() -> BaseClient:
    """Return a BaseClient-compatible mock for items that don't talk to a gateway."""
    return MagicMock(spec=BaseClient)


def make_item(who: Who, where: str, *, client: BaseClient | None = None) -> BaseItem:
    """Instantiate the registered item class for `who` at `where`."""
    bootstrap()
    cls = get_item_type(who)
    if cls is None:
        raise KeyError(f"No item type registered for {who}")
    return cls(client or fake_client(), where)


def parse_events(item: BaseItem, message: BaseMessage) -> list[Event]:
    """Run the registered parser for `item._who` against `message`."""
    bootstrap()
    fn = get_parser(item._who)
    if fn is None:
        raise KeyError(f"No parser registered for {item._who}")
    return list(fn(item, message))


def parse_one_own(item: BaseItem, own: str) -> Event:
    """Parse a raw OWN string into a single event for the given item.

    Convenience for tests: `parse_one_own(light, "*1*1*32##")` returns the
    `LightStatusEvent`.
    """
    msg = parse_message(own)
    events = parse_events(item, msg)
    assert len(events) == 1, f"expected 1 event, got {len(events)}: {events!r}"
    return events[0]
