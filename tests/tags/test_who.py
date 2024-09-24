import pytest

from pyown.tags import Who


def test_who_conversion() -> None:
    # Test if the conversion from WHO to description is working
    assert Who.SCENE.name == "Scene"
    assert Who.LIGHTING.name == "Lighting"
    assert Who.AUTOMATION.name == "Automation"


def test_parsing() -> None:
    # Test if the conversion from string to WHO is working
    assert Who("0") == Who.SCENE
    assert Who("1") == Who.LIGHTING
    assert Who("2") == Who.AUTOMATION

    # Test if it throws an error when the string is not a valid WHO
    with pytest.raises(ValueError):
        Who("invalid")
    with pytest.raises(ValueError):
        Who("1527627")
    with pytest.raises(ValueError):
        Who(-1)
