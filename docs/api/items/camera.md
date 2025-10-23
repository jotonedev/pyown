---
title: Camera/Multimedia System
summary: Camera and video door entry system control.
---

# Camera Module

The camera module provides support for controlling video door entry systems and cameras
through OpenWebNet (WHO = 7).

## Classes

::: pyown.items.camera.Camera
    options:
        show_source: false
        members:
            - receive_video
            - free_resources
            - zoom_in
            - zoom_out
            - increase_x_coordinate
            - decrease_x_coordinate
            - increase_y_coordinate
            - decrease_y_coordinate
            - increase_luminosity
            - decrease_luminosity
            - increase_contrast
            - decrease_contrast
            - increase_color
            - decrease_color
            - increase_quality
            - decrease_quality
            - display_dial
            - on_status_change

::: pyown.items.camera.WhatCamera
    options:
        show_source: false

::: pyown.items.camera.CameraEvents
    options:
        show_source: false

## Camera Addressing

Camera WHERE addresses range from 4000 to 4099:

- `4000`: Camera 00
- `4001`: Camera 01
- `4002`: Camera 02
- ...
- `4099`: Camera 99

## Video Streaming

The OpenWebNet protocol only handles camera control commands. The actual video streaming
is done via HTTP/HTTPS protocol.

After activating a camera with the `receive_video()` command, the JPEG image can be
retrieved from:

```
http://gateway-ip/telecamera.php?CAM_PASSWD=password
```

or

```
https://gateway-ip/telecamera.php?CAM_PASSWD=password
```

If no password is configured, omit the `CAM_PASSWD` parameter (though using a password
is strongly recommended).

## Example Usage

```python
import asyncio
from pyown import Client
from pyown.items.camera import Camera

async def main():
    # Connect to the gateway
    async with Client("192.168.1.35", 20000) as client:
        # Create a camera instance for camera 00 (WHERE = 4000)
        camera = Camera(client, "4000")
        
        # Activate the camera to receive video
        await camera.receive_video()
        
        # Adjust camera settings
        await camera.zoom_in()
        await camera.increase_luminosity()
        await camera.increase_contrast()
        
        # Display a specific dial
        await camera.display_dial(1, 1)  # Display DIAL 1-1
        
        # Free resources when done
        await camera.free_resources()

asyncio.run(main())
```

## Available Commands

### Video Control

- `receive_video()`: Activate the camera to receive video
- `free_resources()`: Free audio and video resources

### Zoom Controls

- `zoom_in()`: Zoom in the camera view
- `zoom_out()`: Zoom out the camera view
- `increase_x_coordinate()`: Move zoom center right
- `decrease_x_coordinate()`: Move zoom center left
- `increase_y_coordinate()`: Move zoom center down
- `decrease_y_coordinate()`: Move zoom center up

### Image Adjustments

- `increase_luminosity()`: Increase brightness
- `decrease_luminosity()`: Decrease brightness
- `increase_contrast()`: Increase contrast
- `decrease_contrast()`: Decrease contrast
- `increase_color()`: Increase color saturation
- `decrease_color()`: Decrease color saturation
- `increase_quality()`: Increase image quality
- `decrease_quality()`: Decrease image quality

### Display Control

- `display_dial(x, y)`: Display a specific dial position (x, y in range 1-4)

## Event Handling

You can register callbacks to be notified when camera events occur:

```python
from pyown.items.camera import Camera, WhatCamera

@Camera.on_status_change
async def handle_camera_event(camera: Camera, what: WhatCamera):
    print(f"Camera {camera.where} event: {what}")
```
