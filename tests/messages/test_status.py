from pyown.messages import StatusRequest, MessageType, parse_message


def test_status_request():
    message = "*#1*12##"

    status_request = parse_message(message)

    assert isinstance(status_request, StatusRequest)
    assert str(status_request) == message
    assert status_request.who == "1"
    assert status_request.where == "12"
    assert status_request.type == MessageType.STATUS_REQUEST


def test_status_request_with_params():
    message = "*#1*41#4#2##"

    status_request = parse_message(message)

    assert isinstance(status_request, StatusRequest)
    assert str(status_request) == message
    assert status_request.who == "1"
    assert status_request.where == "41#4#2"
    assert status_request.where.tag == "41"
    assert status_request.where.parameters == ["4", "2"]
    assert status_request.type == MessageType.STATUS_REQUEST
