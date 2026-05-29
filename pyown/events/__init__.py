"""Event framework for pyown.

Adding a new item type is a single self-contained subdirectory under
`pyown/items/`:

  pyown/items/my_thing/
      __init__.py
      my_thing.py    # @item(Who.X) class MyThing(BaseItem): ...
      events.py      # frozen dataclass Event subclasses + @parser(Who.X) fn

The Client wires the bus up automatically; no central registry to edit.
"""

from .bus import EventBus, Subscription
from .event import Event
from .registry import (
    ParserFn,
    all_whos,
    bootstrap,
    get_item_type,
    get_parser,
    item,
    parser,
)

__all__ = [
    "Event",
    "EventBus",
    "Subscription",
    "ParserFn",
    "parser",
    "item",
    "get_parser",
    "get_item_type",
    "all_whos",
    "bootstrap",
]
