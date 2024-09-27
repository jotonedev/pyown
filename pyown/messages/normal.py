import re
from typing import Self, Pattern, AnyStr, Final

from .base import BaseMessage, MessageType
from ..tags import Who, What, Where

__all__ = [
    "NormalMessage",
]


class NormalMessage(BaseMessage):
    """
    Represent a Normal message

    Syntax: *who*what*where##

    """
    _type: Final[MessageType] = MessageType.NORMAL
    _tags: Final[tuple[Who, What, Where]]

    _regex: Pattern[AnyStr] = re.compile(r"^\*[0-9#]+\*[0-9#]*\*[0-9#]*##$")

    def __init__(self, tags: tuple[Who, What, Where]):
        self._tags = tags

    @property
    def who(self) -> Who:
        return self._tags[0]

    @property
    def what(self) -> What:
        return self._tags[1]

    @property
    def where(self) -> Where:
        return self._tags[2]

    @property
    def message(self) -> str:
        return f"*{self.who}*{self.what}*{self.where}##"

    @classmethod
    def parse(cls, tags: list[str]) -> Self:
        """Parse the tags of a message from the OpenWebNet bus."""

        return cls(
            tags=(
                Who(tags[0]),
                What(tags[1]),
                Where(tags[2])
            )
        )
