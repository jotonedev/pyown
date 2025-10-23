from asyncio import Task
from enum import Enum, StrEnum, auto
from typing import Callable, Coroutine, Final, Self

from ...exceptions import InvalidMessage
from ...messages import BaseMessage, NormalMessage
from ...tags import What, Who
from ..base import BaseItem, CoroutineCallback

__all__ = [
    "Camera",
    "WhatCamera",
    "CameraEvents",
]


class CameraEvents(Enum):
    """
    This enum is used internally to register the callbacks to the correct event.

    Attributes:
        RECEIVE_VIDEO: The event for when receiving video.
        FREE_RESOURCES: The event for when audio/video resources are freed.
        ALL: The event for all events.
    """

    RECEIVE_VIDEO = auto()
    FREE_RESOURCES = auto()
    ALL = auto()  # For all events


class WhatCamera(What, StrEnum):
    """
    This enum contains the possible commands and states for a camera.

    Attributes:
        RECEIVE_VIDEO: Receive video from camera.
        FREE_RESOURCES: Free audio/video resources.
        ZOOM_IN: Zoom in.
        ZOOM_OUT: Zoom out.
        INCREASE_X: Increases X coordinate of the central part of the image to be zoomed.
        DECREASE_X: Decreases X coordinate of the central part of the image to be zoomed.
        INCREASE_Y: Increases Y coordinate of the central part of the image to be zoomed.
        DECREASE_Y: Decreases Y coordinate of the central part of the image to be zoomed.
        INCREASE_LUMINOSITY: Increases luminosity.
        DECREASE_LUMINOSITY: Decreases luminosity.
        INCREASE_CONTRAST: Increases contrast.
        DECREASE_CONTRAST: Decreases contrast.
        INCREASE_COLOR: Increases color.
        DECREASE_COLOR: Decreases color.
        INCREASE_QUALITY: Increases image quality.
        DECREASE_QUALITY: Decreases image quality.
        DISPLAY_DIAL_11: Display DIAL 1-1.
        DISPLAY_DIAL_12: Display DIAL 1-2.
        DISPLAY_DIAL_13: Display DIAL 1-3.
        DISPLAY_DIAL_14: Display DIAL 1-4.
        DISPLAY_DIAL_21: Display DIAL 2-1.
        DISPLAY_DIAL_22: Display DIAL 2-2.
        DISPLAY_DIAL_23: Display DIAL 2-3.
        DISPLAY_DIAL_24: Display DIAL 2-4.
        DISPLAY_DIAL_31: Display DIAL 3-1.
        DISPLAY_DIAL_32: Display DIAL 3-2.
        DISPLAY_DIAL_33: Display DIAL 3-3.
        DISPLAY_DIAL_34: Display DIAL 3-4.
        DISPLAY_DIAL_41: Display DIAL 4-1.
        DISPLAY_DIAL_42: Display DIAL 4-2.
        DISPLAY_DIAL_43: Display DIAL 4-3.
        DISPLAY_DIAL_44: Display DIAL 4-4.
    """

    RECEIVE_VIDEO = "0"
    FREE_RESOURCES = "9"
    ZOOM_IN = "120"
    ZOOM_OUT = "121"
    INCREASE_X = "130"
    DECREASE_X = "131"
    INCREASE_Y = "140"
    DECREASE_Y = "141"
    INCREASE_LUMINOSITY = "150"
    DECREASE_LUMINOSITY = "151"
    INCREASE_CONTRAST = "160"
    DECREASE_CONTRAST = "161"
    INCREASE_COLOR = "170"
    DECREASE_COLOR = "171"
    INCREASE_QUALITY = "180"
    DECREASE_QUALITY = "181"
    DISPLAY_DIAL_11 = "311"
    DISPLAY_DIAL_12 = "312"
    DISPLAY_DIAL_13 = "313"
    DISPLAY_DIAL_14 = "314"
    DISPLAY_DIAL_21 = "321"
    DISPLAY_DIAL_22 = "322"
    DISPLAY_DIAL_23 = "323"
    DISPLAY_DIAL_24 = "324"
    DISPLAY_DIAL_31 = "331"
    DISPLAY_DIAL_32 = "332"
    DISPLAY_DIAL_33 = "333"
    DISPLAY_DIAL_34 = "334"
    DISPLAY_DIAL_41 = "341"
    DISPLAY_DIAL_42 = "342"
    DISPLAY_DIAL_43 = "343"
    DISPLAY_DIAL_44 = "344"


dial_map: Final[dict[tuple[int, int], WhatCamera]] = {
    (1, 1): WhatCamera.DISPLAY_DIAL_11,
    (1, 2): WhatCamera.DISPLAY_DIAL_12,
    (1, 3): WhatCamera.DISPLAY_DIAL_13,
    (1, 4): WhatCamera.DISPLAY_DIAL_14,
    (2, 1): WhatCamera.DISPLAY_DIAL_21,
    (2, 2): WhatCamera.DISPLAY_DIAL_22,
    (2, 3): WhatCamera.DISPLAY_DIAL_23,
    (2, 4): WhatCamera.DISPLAY_DIAL_24,
    (3, 1): WhatCamera.DISPLAY_DIAL_31,
    (3, 2): WhatCamera.DISPLAY_DIAL_32,
    (3, 3): WhatCamera.DISPLAY_DIAL_33,
    (3, 4): WhatCamera.DISPLAY_DIAL_34,
    (4, 1): WhatCamera.DISPLAY_DIAL_41,
    (4, 2): WhatCamera.DISPLAY_DIAL_42,
    (4, 3): WhatCamera.DISPLAY_DIAL_43,
    (4, 4): WhatCamera.DISPLAY_DIAL_44,
}


class Camera(BaseItem):
    """
    Camera items are used to control video door entry systems and cameras.

    The camera system uses WHO = 7 (VIDEO_DOOR_ENTRY) and supports various
    commands for video control, zoom, and image adjustments.

    Note: The actual video streaming is handled via HTTP/HTTPS protocol
    and is not part of this OpenWebNet implementation. After activating
    a camera with receive_video(), the image can be retrieved via:
    http://gateway-ip/telecamera.php?CAM_PASSWD=password
    """

    _who = Who.VIDEO_DOOR_ENTRY

    _event_callbacks: dict[CameraEvents, list[CoroutineCallback]] = {}

    async def receive_video(self):
        """
        Activates the camera to receive video.

        After this command, the video stream can be accessed via HTTP/HTTPS
        at the gateway's telecamera.php endpoint.
        """
        await self.send_normal_message(WhatCamera.RECEIVE_VIDEO)

    async def _send_command_without_where(self, what: WhatCamera):
        """
        Helper method to send commands without WHERE parameter.

        Many camera commands (zoom, adjustments, etc.) do not use WHERE
        and follow the format *7*WHAT## instead of *7*WHAT*WHERE##.

        Args:
            what: The WHAT command to send.
        """
        from ...messages import GenericMessage

        msg = GenericMessage([str(self._who), str(what)])
        await self._send_message(msg)
        resp = await self._read_message()
        self._check_ack(resp)

    async def free_resources(self):
        """
        Frees audio and video resources.

        This command releases the video channel and audio/video resources.
        Note: This command does not use a WHERE parameter.
        """
        await self._send_command_without_where(WhatCamera.FREE_RESOURCES)

    async def zoom_in(self):
        """Zooms in the camera view."""
        await self._send_command_without_where(WhatCamera.ZOOM_IN)

    async def zoom_out(self):
        """Zooms out the camera view."""
        await self._send_command_without_where(WhatCamera.ZOOM_OUT)

    async def increase_x_coordinate(self):
        """Increases X coordinate of the central part of the image to be zoomed."""
        await self._send_command_without_where(WhatCamera.INCREASE_X)

    async def decrease_x_coordinate(self):
        """Decreases X coordinate of the central part of the image to be zoomed."""
        await self._send_command_without_where(WhatCamera.DECREASE_X)

    async def increase_y_coordinate(self):
        """Increases Y coordinate of the central part of the image to be zoomed."""
        await self._send_command_without_where(WhatCamera.INCREASE_Y)

    async def decrease_y_coordinate(self):
        """Decreases Y coordinate of the central part of the image to be zoomed."""
        await self._send_command_without_where(WhatCamera.DECREASE_Y)

    async def increase_luminosity(self):
        """Increases the luminosity of the camera image."""
        await self._send_command_without_where(WhatCamera.INCREASE_LUMINOSITY)

    async def decrease_luminosity(self):
        """Decreases the luminosity of the camera image."""
        await self._send_command_without_where(WhatCamera.DECREASE_LUMINOSITY)

    async def increase_contrast(self):
        """Increases the contrast of the camera image."""
        await self._send_command_without_where(WhatCamera.INCREASE_CONTRAST)

    async def decrease_contrast(self):
        """Decreases the contrast of the camera image."""
        await self._send_command_without_where(WhatCamera.DECREASE_CONTRAST)

    async def increase_color(self):
        """Increases the color saturation of the camera image."""
        await self._send_command_without_where(WhatCamera.INCREASE_COLOR)

    async def decrease_color(self):
        """Decreases the color saturation of the camera image."""
        await self._send_command_without_where(WhatCamera.DECREASE_COLOR)

    async def increase_quality(self):
        """Increases the quality of the camera image."""
        await self._send_command_without_where(WhatCamera.INCREASE_QUALITY)

    async def decrease_quality(self):
        """Decreases the quality of the camera image."""
        await self._send_command_without_where(WhatCamera.DECREASE_QUALITY)

    async def display_dial(self, x: int, y: int):
        """
        Displays a specific dial position.

        Args:
            x: The X dial number (1-4).
            y: The Y dial number (1-4).

        Raises:
            ValueError: If x or y are not in the range 1-4.
        """
        if x not in range(1, 5) or y not in range(1, 5):
            raise ValueError("Dial coordinates must be in range 1-4")

        await self._send_command_without_where(dial_map[(x, y)])

    @classmethod
    def on_status_change(
        cls, callback: Callable[[Self, WhatCamera, BaseMessage], Coroutine[None, None, None]]
    ):
        """
        Registers a callback to be called when the status of the camera changes.

        Args:
            callback (Callable[[Self, WhatCamera, BaseMessage], Coroutine[None, None, None]]): The callback to call.
                It will receive as arguments the item, the WhatCamera value, and the message.
        """
        cls._event_callbacks.setdefault(CameraEvents.ALL, []).append(callback)

    @classmethod
    async def call_callbacks(cls, item: Self, message: BaseMessage) -> list[Task]:
        tasks: list[Task] = []

        if isinstance(message, NormalMessage):
            tasks += cls._create_tasks(
                cls._event_callbacks.get(CameraEvents.ALL, []),
                item,
                WhatCamera(str(message.what)),
                message,
            )
        else:
            raise InvalidMessage(str(message))

        return tasks
