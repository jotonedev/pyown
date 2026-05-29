"""Smoke-test scaffold for the registry: a minimal thermoregulation item.

This file demonstrates that a new item type can be wired in entirely within
its own subdirectory — no central registry edits required. The actual
thermoregulation protocol is much richer than what's modelled here; this is
intentionally a stub.
"""

from ...events import item
from ...tags import Who
from ..base import BaseItem


@item(Who.THERMOREGULATION)
class Thermo(BaseItem):
    """Stub thermoregulation item — placeholder for full protocol support."""
