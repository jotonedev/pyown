from enum import Enum, auto

from .base import TagWithParameters

__all__ = [
    "Where",
    "WhereType"
]


class WhereType(Enum):
    """
    Enum for the type of the WHERE tag.

    Attributes:
        GENERAL: it refers to all devices connected to all bus connected to the gateway
            (usually a gateway supports only one bus).
        AMBIENT: usually an ambient is a room, but it depends on how the devices where configured.
        LIGHT_POINT: it refers to a single device.
        GROUP: it refers to a group of devices.
        LOCAL_BUS: it refers to all devices connected to a specific bus.
    """
    GENERAL = auto()
    AMBIENT = auto()
    LIGHT_POINT = auto()
    GROUP = auto()
    LOCAL_BUS = auto()


class Where(TagWithParameters):
    """
    Represents the WHERE tag.

    The tag WHERE is the address on the bus for the related device.
    This can indicate, also, a group of devices or a local bus.
    """

    @property
    def type(self) -> WhereType:
        """
        Gets what the where tag indicates to.

        Returns:
            WhereType: The type of the WHERE tag.
        """
        # TODO: Refactor this method and write tests for it.
        if self.string == "0":
            return WhereType.GENERAL
        elif self.string in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            return WhereType.AMBIENT
        elif self.string in ["00", "100"]:
            return WhereType.AMBIENT
        elif self.string.startswith(("00", "10")):
            return WhereType.LIGHT_POINT
        elif self.string.startswith(("1", "2", "3", "4", "5", "6", "7", "8", "9")):
            return WhereType.LIGHT_POINT
        elif self.string.startswith(("01", "02", "03", "04", "05", "06", "07", "08", "09")):
            return WhereType.LIGHT_POINT
        elif self.tag == "" and len(self.parameters) == 1:
            return WhereType.GROUP
        elif self.tag == "" and len(self.parameters) == 2:
            return WhereType.LOCAL_BUS
        else:
            raise ValueError(f"Invalid WHERE tag: {self.string}")
