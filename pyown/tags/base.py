from typing import Final

from ..exceptions import InvalidTag

__all__ = [
    "Tag",
    "TagWithParameters",
    "Value",
]

VALID_TAG_CHARS: Final[str] = "0123456789#"


class Tag(str):
    """Tag class."""

    def __init__(self, string: str = ""):
        # Check if the string contains only valid characters
        if not all(c in VALID_TAG_CHARS for c in string):
            raise InvalidTag(string)

        super().__init__()

    @property
    def tag(self) -> int | None:
        """Return the value of the tag without its parameters or prefix"""
        val = self.removeprefix("#")
        if len(val) > 0:
            return int(val)
        else:
            return None

    @property
    def parameters(self) -> list[str] | None:
        """Return the parameters of the tag"""
        return None


class TagWithParameters(Tag):
    @property
    def tag(self) -> int | None:
        """Return the value of the tag without its parameters or prefix"""
        val = self.split("#")[0]
        if len(val) > 0:
            return int(val)
        else:
            return None

    @property
    def parameters(self) -> list[str]:
        """Return the parameters of the tag"""
        return self.split("#")[1:]


class Value(Tag):
    """
    Represent a value tag in a dimension response message.
    """
    pass
