from pyown.messages import NACK, MessageType, parse_message


def test_nack():
    message = "*#*0##"

    nack = parse_message(message)

    assert isinstance(nack, NACK)
    assert str(nack) == message
    assert nack.tags == ("#", "0")
    assert nack.type == MessageType.NACK
    assert NACK() == nack
