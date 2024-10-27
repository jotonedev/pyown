from typing import Type, Final

from .automation import Automation
from .base import BaseItem
from .gateway import Gateway
from .lighting import Light
from ..tags import Who

__all__ = [
    "ITEM_TYPES"
]

ITEM_TYPES: Final[dict[Who, Type[BaseItem]]] = {
    Who.LIGHTING: Light,
    Who.AUTOMATION: Automation,
    Who.GATEWAY: Gateway
}
"""A dictionary that maps the Who tag to the corresponding item class."""
