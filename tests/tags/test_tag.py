import pytest

from pyown.exceptions import InvalidTag
from pyown.tags.base import TagWithParameters, Tag


def test_tag_with_params() -> None:
    # Check if value is correctly parsed
    tag = TagWithParameters("123")
    assert tag.tag == "123"
    assert tag.parameters == []
    assert tag == "123"

    # Check if parameters are correctly parsed
    tag = TagWithParameters("123#512#123#1#22#1213")
    assert tag.tag == "123"
    assert tag.parameters == ["512", "123", "1", "22", "1213"]
    assert tag == "123#512#123#1#22#1213"

    # Check if tag is parsed when value is missing
    tag = TagWithParameters("#512#123#1#22#1213")
    assert tag.tag == ""

    # Check the empty tag
    tag = TagWithParameters("")
    assert tag.tag == ""
    assert tag.parameters == []
    assert tag == ""

    # Check if invalid characters raise an exception
    with pytest.raises(InvalidTag):
        TagWithParameters("123#512#123#-1")

    with pytest.raises(InvalidTag):
        TagWithParameters("123#param1#param2")

    with pytest.raises(InvalidTag):
        TagWithParameters("#param1#param2")


def test_tag() -> None:
    tag = Tag("123")
    assert tag.tag == "123"
    assert tag.parameters is None
    assert tag == "123"

    # In some type of messages the tag is prefixed with a hash even if it doesn't allow for parameters
    tag = Tag("#123")
    assert tag.tag == "123"
    assert tag.parameters is None
    assert tag == "#123"

    # Check the empty tag
    tag = Tag("")
    assert tag.tag == ""
    assert tag.parameters is None
    assert tag == ""

    # Check if invalid characters raise an exception
    with pytest.raises(InvalidTag):
        Tag("123sjkkw")


def test_conversion_to_params_tag() -> None:
    tag = Tag("123")

    assert tag.with_parameter("1") == TagWithParameters("123#1")

    tag = TagWithParameters("123#1")
    assert tag.with_parameter("1") == TagWithParameters("123#1#1")

    tag = tag.with_parameter("1")
    assert tag == TagWithParameters("123#1#1")
