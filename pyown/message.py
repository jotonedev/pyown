from dataclasses import dataclass, field
from typing import Self, Final, Type

from .constants.who import WHO


__all__ = [
    "OWNMessage",
    "RawMessage", 
    "NormalMessage", 
    "StatusRequest", 
    "DimensionRequest",
    "DimensionResponse", 
    "ACK", 
    "NACK",
]


@dataclass
class RawMessage:
    """Represent a message sent or received from the OpenWebNet bus."""
    tags: list[str]

    @classmethod
    def parse(cls, msg: str) -> Self:
        """Parse a message from the OpenWebNet bus."""
        msg = msg.strip().removesuffix("##").removeprefix("*")
        tags = msg.split("*")

        return cls._tags_parse(tags)
    
    @classmethod
    def _tags_parse(cls, tags: list[str]) -> Self:
        """Parse the tags of a message from the OpenWebNet bus."""
        return cls(tags=tags)


    def __str__(self) -> str:
        """Return the message as a string."""
        return "*" + "*".join(self.tags) + "##"
    
    def __eq__(self, value: object) -> bool:
        """Return True if the value is equal to the message."""
        if not isinstance(value, RawMessage):
            return False
        return self.tags == value.tags


OWNMessage = Type[RawMessage]


ACK: Final = RawMessage(tags=["#", "1"])
NACK: Final = RawMessage(tags=["#", "0"])


@dataclass
class NormalMessage(RawMessage):
    """Represent a normal message"""
    who: WHO
    what: str
    where: str

    @classmethod
    def _tags_parse(cls, tags: list[str]) -> Self:
        """Parse the tags of a message from the OpenWebNet bus."""
        who, what, where = tags
        return cls(who=who, what=what, where=where)

@dataclass
class StatusRequest(RawMessage):
    """Represent a status message"""
    who: WHO
    where: str

    @classmethod
    def _tags_parse(cls, tags: list[str]) -> Self:
        """Parse the tags of a message from the OpenWebNet bus."""
        who, where = tags
        return cls(who=who, where=where)


@dataclass
class DimensionRequest(RawMessage):
    """Represent a dimension message"""
    who: WHO
    where: str
    dimension: str


    @classmethod
    def _tags_parse(cls, tags: list[str]) -> Self:
        """Parse the tags of a message from the OpenWebNet bus."""
        who, where, dimension = tags
        return cls(who=who, where=where, dimension=dimension)
    
@dataclass
class DimensionResponse(RawMessage):
    """Represent a dimension message"""
    who: WHO
    where: str
    dimension: str
    values: list[str]

    @classmethod
    def _tags_parse(cls, tags: list[str]) -> Self:
        """Parse the tags of a message from the OpenWebNet bus."""
        who, where, dimension, *values = tags
        return cls(who=who, where=where, dimension=dimension, values=values)
    