from enum import Enum, auto

from .base import TagWithParameters

__all__ = [
    "Where",
    "WhereType"
]


class WhereType(Enum):
    GENERAL = auto()
    AMBIENT = auto()
    LIGHT_POINT = auto()
    GROUP = auto()
    LOCAL_BUS = auto()


class Where(TagWithParameters):
    """
    Represent the WHERE tag.

    The tag WHERE detects the objects involved by the frame (environment, room, single
    object, whole system).
    """

    @property
    def type(self) -> WhereType:
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
