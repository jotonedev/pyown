from pyown.messages import GenericMessage, parse_message


def test_generic():
    msg = "*98*1##"

    generic_message = parse_message(msg)

    assert isinstance(generic_message, GenericMessage)
    assert str(generic_message) == msg
    assert generic_message.tags == ["98", "1"]
