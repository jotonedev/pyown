from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from ..items.base import BaseItem
    from ..tags import Where

__all__ = ["Event", "E"]


@dataclass(frozen=True, slots=True)
class Event:
    """Base class for all events dispatched on the EventBus.

    Subclasses are frozen dataclasses with typed payload fields. Every event
    carries the originating item and its where tag.
    """

    item: "BaseItem"
    where: "Where"


E = TypeVar("E", bound=Event)
