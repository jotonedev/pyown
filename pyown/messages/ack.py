import re
from typing import Self, Pattern, AnyStr, Final

from .base import BaseMessage, MessageType
from ..exceptions import ParseError

__all__ = [
    "ACK",
]


class ACK(BaseMessage):
    """
    Represent an ACK message

    Syntax: *#*1##
    """
    _type: Final[MessageType] = MessageType.ACK
    _tags: Final[tuple[str]] = ("#", "1")

    _regex: Pattern[AnyStr] = re.compile(r"^\*#\*1##$")

    def __init__(self):
        pass

    @property
    def message(self) -> str:
        return "*#*1##"

    @classmethod
    def parse(cls, tags: list[str]) -> Self:
        """Parse the tags of a message from the OpenWebNet bus."""
        # the first tag bust be #
        if tags[0] != "#" and tags[1] != "1":
            raise ParseError(tags=tags, message="Invalid ACK message")

        return cls()
