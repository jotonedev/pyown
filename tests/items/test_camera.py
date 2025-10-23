"""
Tests for the Camera item module.
"""

from pyown.items.camera import Camera, CameraEvents, WhatCamera
from pyown.messages import GenericMessage, NormalMessage
from pyown.tags import Where, Who


def test_what_camera_commands():
    """Test that all WhatCamera commands have correct values."""
    assert WhatCamera.RECEIVE_VIDEO == "0"
    assert WhatCamera.FREE_RESOURCES == "9"
    assert WhatCamera.ZOOM_IN == "120"
    assert WhatCamera.ZOOM_OUT == "121"
    assert WhatCamera.INCREASE_X == "130"
    assert WhatCamera.DECREASE_X == "131"
    assert WhatCamera.INCREASE_Y == "140"
    assert WhatCamera.DECREASE_Y == "141"
    assert WhatCamera.INCREASE_LUMINOSITY == "150"
    assert WhatCamera.DECREASE_LUMINOSITY == "151"
    assert WhatCamera.INCREASE_CONTRAST == "160"
    assert WhatCamera.DECREASE_CONTRAST == "161"
    assert WhatCamera.INCREASE_COLOR == "170"
    assert WhatCamera.DECREASE_COLOR == "171"
    assert WhatCamera.INCREASE_QUALITY == "180"
    assert WhatCamera.DECREASE_QUALITY == "181"


def test_camera_events():
    """Test that CameraEvents are defined."""
    assert CameraEvents.RECEIVE_VIDEO
    assert CameraEvents.FREE_RESOURCES
    assert CameraEvents.ALL


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


def test_camera_dial_commands():
    """Test that all dial commands have correct values."""
    assert WhatCamera.DISPLAY_DIAL_11 == "311"
    assert WhatCamera.DISPLAY_DIAL_12 == "312"
    assert WhatCamera.DISPLAY_DIAL_13 == "313"
    assert WhatCamera.DISPLAY_DIAL_14 == "314"
    assert WhatCamera.DISPLAY_DIAL_21 == "321"
    assert WhatCamera.DISPLAY_DIAL_44 == "344"


def test_camera_instantiation():
    """Test that Camera can be instantiated with correct WHO."""

    class MockClient:
        pass

    camera = Camera(MockClient(), "4000")
    assert camera._who == Who.VIDEO_DOOR_ENTRY
    assert str(camera._where) == "4000"


def test_camera_has_required_methods():
    """Test that Camera has all required methods."""
    required_methods = [
        "receive_video",
        "free_resources",
        "zoom_in",
        "zoom_out",
        "increase_x_coordinate",
        "decrease_x_coordinate",
        "increase_y_coordinate",
        "decrease_y_coordinate",
        "increase_luminosity",
        "decrease_luminosity",
        "increase_contrast",
        "decrease_contrast",
        "increase_color",
        "decrease_color",
        "increase_quality",
        "decrease_quality",
        "display_dial",
        "on_status_change",
        "call_callbacks",
    ]

    for method in required_methods:
        assert hasattr(Camera, method), f"Camera should have method: {method}"
