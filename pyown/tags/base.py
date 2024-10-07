from typing import Final

from ..exceptions import InvalidTag

__all__ = [
    "Tag",
    "TagWithParameters",
    "Value",
]

VALID_TAG_CHARS: Final[str] = "0123456789#"


class Tag:
    """Tag class."""

    def __init__(self, string: str = "", *args, **kwargs):
        # Check if the string contains only valid characters
        if not all(c in VALID_TAG_CHARS for c in string):
            raise InvalidTag(string)

        self._string = string

    @property
    def string(self) -> str:
        """Return the value of the tag"""
        return self._string

    @property
    def tag(self) -> str | None:
        """Return the value of the tag without its parameters or prefix"""
        val = self.string.removeprefix("#")
        return val

    @property
    def parameters(self) -> list[str] | None:
        """Return the parameters of the tag"""
        return None

    def with_parameters(self, *parameters: str | int) -> "TagWithParameters":
        """Return the tag with parameters"""
        return TagWithParameters(f"{self}#{'#'.join(parameters)}")

    def __str__(self) -> str:
        return self.string

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.string})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Tag):
            return self.string == other.string
        elif isinstance(other, str):
            return self.string == other
        else:
            return NotImplemented

    def __hash__(self) -> int:
        return hash(self.string)


class TagWithParameters(Tag):
    @property
    def tag(self) -> str:
        """Return the value of the tag without its parameters or prefix"""
        val = self.string.split("#")[0]
        return val

    @property
    def parameters(self) -> list[str]:
        """Return the parameters of the tag"""
        return self.string.split("#")[1:]


class Value(Tag):
    """
    Represent a value tag in a dimension response message.
    """
    pass
