from pyown.messages import NormalMessage, MessageType, parse_message


def test_normal():
    msg = "*1*1*12##"

    normal = parse_message(msg)

    assert isinstance(normal, NormalMessage)
    assert str(normal) == msg
    assert normal.who == "1"
    assert normal.what == "1"
    assert normal.where == "12"
    assert normal.type == MessageType.NORMAL


def test_normal_with_params():
    msg = "*2*1*41#4#2##"

    normal = parse_message(msg)

    assert isinstance(normal, NormalMessage)
    assert str(normal) == msg
    assert normal.who == "2"
    assert normal.what == "1"
    assert normal.where == "41#4#2"
    assert normal.where.tag == "41"
    assert normal.where.parameters == ["4", "2"]
    assert normal.type == MessageType.NORMAL
