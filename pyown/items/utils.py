from typing import Final, Type

from ..tags import Who
from .automation import Automation
from .base import BaseItem
from .energy.energy import EnergyManagement
from .gateway import Gateway
from .lighting import Light

__all__ = ["ITEM_TYPES"]

ITEM_TYPES: Final[dict[Who, Type[BaseItem]]] = {
    Who.LIGHTING: Light,
    Who.AUTOMATION: Automation,
    Who.GATEWAY: Gateway,
    Who.ENERGY_MANAGEMENT: EnergyManagement,
}
"""A dictionary that maps the Who tag to the corresponding item class."""
