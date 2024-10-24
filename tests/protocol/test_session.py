from pyown.client.session import SessionType


def test_session_type_message_generation():
    cmd_session = SessionType.CommandSession
    assert cmd_session.to_message().message == "*99*9##"

    event_session = SessionType.EventSession
    assert event_session.to_message().message == "*99*1##"

    old_cmd_session = SessionType.OldCommandSession
    assert old_cmd_session.to_message().message == "*99*0##"
