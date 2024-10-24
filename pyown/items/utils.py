from typing import Type, Final

from .base import BaseItem
from .lighting import Light
from ..tags import Who

__all__ = [
    "ITEM_TYPES"
]


ITEM_TYPES: Final[dict[Who, Type[BaseItem]]] = {
    Who.LIGHTING: Light,
}
"""A dictionary that maps the Who tag to the corresponding item class."""
