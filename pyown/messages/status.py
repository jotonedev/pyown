import re
from typing import Self, Pattern

from .base import BaseMessage, MessageType
from ..tags import Who, Where

__all__ = [
    "StatusRequest"
]


class StatusRequest(BaseMessage):
    """
    Represents a status request message

    Syntax: `*#who*where##`
    """
    _type: MessageType = MessageType.STATUS_REQUEST
    _tags: tuple[Who, Where]

    _regex: Pattern[str] = re.compile(r"^\*#[0-9#]+\*[0-9]*(?:#[0-9]*)*##$")

    def __init__(self, tags: tuple[Who, Where]):
        self._tags = tags

    @property
    def who(self) -> Who:
        return self._tags[0]

    @property
    def where(self) -> Where:
        return self._tags[1]

    @property
    def message(self) -> str:
        return f"*#{self.who}*{self.where}##"

    @classmethod
    def parse(cls, tags: list[str]) -> Self:
        """Parses the tags of a message from the OpenWebNet bus."""

        return cls(
            tags=(
                Who(tags[0].removeprefix("#")),
                Where(tags[1])
            )
        )
