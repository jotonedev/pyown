import asyncio
import logging
from typing import Awaitable, Callable, cast

from ..tags import Where
from .event import E, Event

__all__ = ["EventBus", "Subscription"]

log = logging.getLogger("pyown.events.bus")

Handler = Callable[[Event], Awaitable[None]]


class Subscription:
    """Handle returned by `EventBus.subscribe`. Use `unsubscribe()` to remove
    the handler, or treat the subscription as a context manager.
    """

    __slots__ = ("_bus", "_event_type", "_active", "_is_all")

    def __init__(self, bus: "EventBus", event_type: type[Event] | None, *, is_all: bool):
        self._bus = bus
        self._event_type = event_type
        self._is_all = is_all
        self._active = True

    def unsubscribe(self) -> None:
        if not self._active:
            return
        self._active = False
        if self._is_all:
            self._bus._all_subs[:] = [s for s in self._bus._all_subs if s.sub is not self]
        else:
            assert self._event_type is not None
            bucket = self._bus._subs.get(self._event_type, [])
            self._bus._subs[self._event_type] = [s for s in bucket if s.sub is not self]

    def __enter__(self) -> "Subscription":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.unsubscribe()


class _Entry:
    __slots__ = ("handler", "where", "sub")

    def __init__(self, handler: Handler, where: str | None, sub: Subscription):
        self.handler = handler
        self.where = where
        self.sub = sub


class EventBus:
    """In-memory typed pub/sub bus for events emitted by the OpenWebNet client.

    Handlers are async callables. They are scheduled as independent tasks so a
    slow or failing handler cannot block sibling handlers or the bus itself.
    """

    def __init__(self) -> None:
        self._subs: dict[type[Event], list[_Entry]] = {}
        self._all_subs: list[_Entry] = []

    def subscribe(
        self,
        event_type: type[E],
        handler: Callable[[E], Awaitable[None]],
        *,
        where: Where | str | None = None,
    ) -> Subscription:
        """Subscribe `handler` to events of `event_type` (or any subclass).

        If `where` is given, the handler only fires for events whose `where`
        tag matches by string equality. This lets callers scope to a single
        light, a single shutter, etc.
        """
        sub = Subscription(self, event_type, is_all=False)
        entry = _Entry(cast(Handler, handler), _normalize_where(where), sub)
        self._subs.setdefault(event_type, []).append(entry)
        return sub

    def subscribe_all(
        self, handler: Callable[[Event], Awaitable[None]]
    ) -> Subscription:
        """Subscribe `handler` to every event dispatched on the bus."""
        sub = Subscription(self, None, is_all=True)
        entry = _Entry(cast(Handler, handler), None, sub)
        self._all_subs.append(entry)
        return sub

    async def dispatch(self, event: Event) -> None:
        """Fan an event out to every matching handler.

        Each handler runs as its own task. Exceptions are logged but do not
        propagate or affect siblings.
        """
        targets: list[Handler] = []

        for registered_type, bucket in self._subs.items():
            if not isinstance(event, registered_type):
                continue
            for entry in bucket:
                if entry.where is not None and entry.where != str(event.where):
                    continue
                targets.append(entry.handler)

        for entry in self._all_subs:
            targets.append(entry.handler)

        if not targets:
            return

        await asyncio.gather(
            *(self._run(handler, event) for handler in targets),
            return_exceptions=False,
        )

    @staticmethod
    async def _run(handler: Handler, event: Event) -> None:
        try:
            await handler(event)
        except Exception as e:
            log.error(
                "Error in event handler %s for %s: %s",
                getattr(handler, "__qualname__", repr(handler)),
                type(event).__name__,
                e,
                exc_info=e,
            )


def _normalize_where(where: Where | str | None) -> str | None:
    if where is None:
        return None
    return str(where)
