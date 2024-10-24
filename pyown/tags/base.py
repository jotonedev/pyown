from typing import Final, Self

from ..exceptions import InvalidTag

__all__ = [
    "Tag",
    "TagWithParameters",
    "Value",
    "is_valid_tag",
    "VALID_TAG_CHARS",
]

VALID_TAG_CHARS: Final[str] = "0123456789#"
"""This are the only valid characters for a tag"""


def is_valid_tag(tag: str) -> bool:
    """
    Checks if the tag is valid.

    A tag is valid if it contains only the characters defined in the VALID_TAG_CHARS constant.

    Args:
        tag (str): The tag to check

    Returns:
        bool: True if the tag is valid, False otherwise
    """
    return all(c in VALID_TAG_CHARS for c in tag)


class Tag:
    """
    Tag class.

    This a base class for all the other types of tags.
    This class does not support parameters. To use parameters, use the TagWithParameters class.
    """

    # noinspection PyUnusedLocal
    def __init__(self, string: str | int = "", *args, **kwargs):
        if isinstance(string, int):
            self._string = str(string)
        else:
            self._string = string

        # Check if the string contains only valid characters
        if not is_valid_tag(self._string):
            raise InvalidTag(self._string)

    @property
    def string(self) -> str:
        """Returns the value of the tag"""
        return self._string

    @property
    def tag(self) -> str | None:
        """Returns the value of the tag without its parameters or prefix"""
        val = self.string.removeprefix("#")
        return val

    @property
    def parameters(self) -> list[str] | None:
        """
        Returns the parameters of the tag.
        For a tag without parameters, this function returns None.
        """
        return None

    def with_parameter(self, parameter: str | int) -> "TagWithParameters":
        """Returns the tag with the specified parameter"""
        return TagWithParameters(f"{self}#{parameter}")

    def __str__(self) -> str:
        return self.string

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.string})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Tag):
            return self.string == other.string
        elif isinstance(other, str):
            return self.string == other
        elif isinstance(other, int):
            return self.string == str(other)
        else:
            return NotImplemented

    def __hash__(self) -> int:
        return hash(self.string)


class TagWithParameters(Tag):
    """
    Tag with parameters.

    A tag with parameters is a tag that contains a value and a list of parameters.
    So, it follows the following format value#parameter1#parameter2#...#parameterN
    """

    @property
    def tag(self) -> str:
        """Returns the value of the tag without its parameters or prefix"""
        val = self.string.split("#")[0]
        return val

    @property
    def parameters(self) -> list[str]:
        """Returns the parameters of the tag"""
        return self.string.split("#")[1:]

    def with_parameter(self, parameter: str | int) -> Self:
        """Returns the tag with the specified parameter"""
        return self.__class__(f"{self}#{parameter}")


class Value(Tag):
    """
    Represents a value tag in a dimension response message.
    """
    pass
