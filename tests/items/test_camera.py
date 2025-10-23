from pyown.items.camera import Camera, WhatCamera
from pyown.messages import GenericMessage, NormalMessage
from pyown.tags import Where, Who


def test_camera_receive_video_message_format():
    """Test that receive_video generates correct message format with WHERE."""
    msg = NormalMessage((Who.VIDEO_DOOR_ENTRY, WhatCamera.RECEIVE_VIDEO, Where("4000")))
    assert msg.message == "*7*0*4000##"


def test_camera_zoom_message_format():
    """Test that zoom commands generate correct message format without WHERE."""
    msg = GenericMessage([str(Who.VIDEO_DOOR_ENTRY), str(WhatCamera.ZOOM_IN)])
    assert msg.message == "*7*120##"


def test_camera_free_resources_message_format():
    """Test that free_resources generates correct message format without WHERE."""
    msg = GenericMessage([str(Who.VIDEO_DOOR_ENTRY), str(WhatCamera.FREE_RESOURCES)])
    assert msg.message == "*7*9##"


def test_camera_instantiation():
    """Test that Camera can be instantiated with correct WHO."""

    class MockClient:
        pass

    camera = Camera(MockClient(), "4000")
    assert camera._who == Who.VIDEO_DOOR_ENTRY
    assert str(camera._where) == "4000"
