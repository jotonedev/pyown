import importlib
import logging
import pkgutil
from typing import TYPE_CHECKING, Callable, Iterable

from ..tags import Who
from .event import Event

if TYPE_CHECKING:
    from ..items.base import BaseItem
    from ..messages import BaseMessage

__all__ = [
    "ParserFn",
    "parser",
    "item",
    "get_parser",
    "get_item_type",
    "bootstrap",
    "all_whos",
]

log = logging.getLogger("pyown.events.registry")

ParserFn = Callable[["BaseItem", "BaseMessage"], Iterable[Event]]

_parsers: dict[Who, ParserFn] = {}
_item_types: dict[Who, type["BaseItem"]] = {}

_bootstrapped = False


def parser(who: Who) -> Callable[[ParserFn], ParserFn]:
    """Register a message-to-event parser for a given WHO tag.

    The parser yields zero or more typed Event instances for each message it
    receives. It is the single source of truth for how a message of this WHO
    becomes events.
    """

    def deco(fn: ParserFn) -> ParserFn:
        if who in _parsers and _parsers[who] is not fn:
            raise RuntimeError(f"Duplicate parser registration for {who}")
        _parsers[who] = fn
        return fn

    return deco


def item(who: Who) -> Callable[[type["BaseItem"]], type["BaseItem"]]:
    """Register an item class for a given WHO tag and set its `_who` attribute.

    The Client uses this to resolve which item class to instantiate for an
    incoming message of a particular WHO.
    """

    def deco(cls: type["BaseItem"]) -> type["BaseItem"]:
        if who in _item_types and _item_types[who] is not cls:
            raise RuntimeError(f"Duplicate item registration for {who}")
        cls._who = who
        _item_types[who] = cls
        return cls

    return deco


def get_parser(who: Who) -> ParserFn | None:
    """Return the registered parser for a WHO, or None."""
    return _parsers.get(who)


def get_item_type(who: Who) -> type["BaseItem"] | None:
    """Return the registered item class for a WHO, or None."""
    return _item_types.get(who)


def all_whos() -> set[Who]:
    """Return the set of WHOs that have both an item class and a parser registered."""
    return set(_item_types) & set(_parsers)


def bootstrap() -> None:
    """Import every `pyown.items.<name>` subpackage to trigger decorator-based
    registration. Idempotent.

    A new item type is wired in by dropping a subdirectory under `pyown/items/`
    that exposes an item class with `@item(...)` and a parser with `@parser(...)`.
    No central edits required.
    """
    global _bootstrapped
    if _bootstrapped:
        return

    from .. import items as items_pkg

    for mod_info in pkgutil.iter_modules(items_pkg.__path__):
        if not mod_info.ispkg:
            continue
        pkg_name = f"{items_pkg.__name__}.{mod_info.name}"
        try:
            importlib.import_module(pkg_name)
        except Exception as e:
            log.warning("Failed to import item package %s: %s", pkg_name, e)
            continue
        # Importing the package may not import its sibling events module if it
        # was not re-exported. Try importing `.events` defensively.
        events_name = f"{pkg_name}.events"
        try:
            importlib.import_module(events_name)
        except ModuleNotFoundError:
            log.debug("No events module for %s", pkg_name)
        except Exception as e:
            log.warning("Failed to import %s: %s", events_name, e)

    _bootstrapped = True


def _reset_for_tests() -> None:
    """Test-only hook to clear registries. Do not call from production code."""
    global _bootstrapped
    _parsers.clear()
    _item_types.clear()
    _bootstrapped = False
