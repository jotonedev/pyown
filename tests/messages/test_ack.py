from pyown.messages import ACK, MessageType, parse_message


def test_nack():
    message = "*#*1##"

    ack = parse_message(message)

    assert isinstance(ack, ACK)
    assert str(ack) == message
    assert ack.tags == ("#", "1")
    assert ack.type == MessageType.ACK
    assert ACK() == ack
