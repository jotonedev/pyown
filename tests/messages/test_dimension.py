from pyown.messages import (
    DimensionRequest,
    DimensionWriting,
    DimensionResponse,
    MessageType,
    parse_message,
)


def test_dimension_request():
    msg = "*#13**1##"

    dimension_request = parse_message(msg)

    assert isinstance(dimension_request, DimensionRequest)
    assert str(dimension_request) == msg
    assert dimension_request.who == "13"
    assert dimension_request.where == ""
    assert dimension_request.dimension == "1"
    assert dimension_request.type == MessageType.DIMENSION_REQUEST


def test_dimension_request_with_params():
    msg = "*#13*7#3*1##"  # not a real message

    dimension_request = parse_message(msg)

    assert isinstance(dimension_request, DimensionRequest)
    assert str(dimension_request) == msg
    assert dimension_request.who == "13"
    assert dimension_request.where == "7#3"
    assert dimension_request.where.tag == "7"
    assert dimension_request.where.parameters == ["3"]
    assert dimension_request.dimension == "1"
    assert dimension_request.type == MessageType.DIMENSION_REQUEST


def test_dimension_writing():
    msg = "*#13**#0*21*10*00*01##"

    dimension_writing = parse_message(msg)

    assert isinstance(dimension_writing, DimensionWriting)
    assert str(dimension_writing) == msg
    assert dimension_writing.who == "13"
    assert dimension_writing.where == ""
    assert dimension_writing.dimension == "0"
    assert dimension_writing.values == ("21", "10", "00", "01")
    assert dimension_writing.type == MessageType.DIMENSION_WRITING


# noinspection DuplicatedCode
def test_dimension_writing_with_params():
    msg = "*#13*7#3*#0*21*10*00*01##"

    dimension_writing = parse_message(msg)

    assert isinstance(dimension_writing, DimensionWriting)
    assert str(dimension_writing) == msg
    assert dimension_writing.who == "13"
    assert dimension_writing.where == "7#3"
    assert dimension_writing.where.tag == "7"
    assert dimension_writing.where.parameters == ["3"]
    assert dimension_writing.dimension == "0"
    assert dimension_writing.values == ("21", "10", "00", "01")
    assert dimension_writing.type == MessageType.DIMENSION_WRITING


def test_dimension_response():
    msg = "*#13**1*1*1*1*2012##"

    dimension_response = parse_message(msg)

    assert isinstance(dimension_response, DimensionResponse)
    assert str(dimension_response) == msg
    assert dimension_response.who == "13"
    assert dimension_response.where == ""
    assert dimension_response.dimension == "1"
    assert dimension_response.values == ("1", "1", "1", "2012")
    assert dimension_response.type == MessageType.DIMENSION_RESPONSE


# noinspection DuplicatedCode
def test_dimension_response_with_params():
    msg = "*#13*7#3*1*1*1*1*2012##"

    dimension_response = parse_message(msg)

    assert isinstance(dimension_response, DimensionResponse)
    assert str(dimension_response) == msg
    assert dimension_response.who == "13"
    assert dimension_response.where == "7#3"
    assert dimension_response.where.tag == "7"
    assert dimension_response.where.parameters == ["3"]
    assert dimension_response.dimension == "1"
    assert dimension_response.values == ("1", "1", "1", "2012")
    assert dimension_response.type == MessageType.DIMENSION_RESPONSE
