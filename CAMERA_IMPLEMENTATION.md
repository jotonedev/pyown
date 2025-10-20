# Camera System Implementation Summary

## Overview
This implementation adds support for the OpenWebNet Camera/Multimedia system (WHO = 7) to the pyown library. The implementation allows control of video door entry systems and cameras through the OpenWebNet protocol.

## Files Created

### 1. Core Module
- **pyown/items/camera/camera.py** - Main camera implementation
  - `Camera` class: Controls camera devices
  - `WhatCamera` enum: Defines all camera commands (32 commands total)
  - `CameraEvents` enum: Defines callback event types

- **pyown/items/camera/__init__.py** - Module exports

### 2. Documentation
- **docs/api/items/camera.md** - API documentation with examples and usage guide

### 3. Example
- **examples/camera_01/** - Working example demonstrating camera control
  - main.py: Example code showing how to use the Camera class
  - README.md: Description of the example

### 4. Tests
- **tests/items/test_camera.py** - Unit tests for camera functionality

### 5. Integration
- **pyown/items/__init__.py** - Updated to export camera module

## Implementation Details

### Commands Supported

#### Video Control
- `receive_video()` - Activate camera to receive video (WHAT=0, requires WHERE)
- `free_resources()` - Free audio/video resources (WHAT=9, no WHERE)

#### Zoom Controls
- `zoom_in()` - Zoom in (WHAT=120)
- `zoom_out()` - Zoom out (WHAT=121)
- `increase_x_coordinate()` - Move zoom center right (WHAT=130)
- `decrease_x_coordinate()` - Move zoom center left (WHAT=131)
- `increase_y_coordinate()` - Move zoom center down (WHAT=140)
- `decrease_y_coordinate()` - Move zoom center up (WHAT=141)

#### Image Adjustments
- `increase_luminosity()` / `decrease_luminosity()` - Adjust brightness (WHAT=150/151)
- `increase_contrast()` / `decrease_contrast()` - Adjust contrast (WHAT=160/161)
- `increase_color()` / `decrease_color()` - Adjust color saturation (WHAT=170/171)
- `increase_quality()` / `decrease_quality()` - Adjust image quality (WHAT=180/181)

#### Display Control
- `display_dial(x, y)` - Display specific dial position (WHAT=3XY, where X,Y = 1-4)

### Message Format Handling

The implementation correctly handles two different message formats:

1. **With WHERE parameter** (for receive_video):
   ```
   *7*0*4000##  (WHO=7, WHAT=0, WHERE=4000)
   ```
   Uses `NormalMessage` class.

2. **Without WHERE parameter** (for zoom, adjustments, etc.):
   ```
   *7*120##  (WHO=7, WHAT=120)
   ```
   Uses `GenericMessage` class via `_send_command_without_where()` helper method.

### Camera Addressing

Cameras are addressed using WHERE values 4000-4099:
- 4000 = Camera 00
- 4001 = Camera 01
- ...
- 4099 = Camera 99

### Video Streaming

Note: The OpenWebNet protocol only handles camera control commands. Actual video streaming is done via HTTP/HTTPS:
```
http://gateway-ip/telecamera.php?CAM_PASSWD=password
```

After activating a camera with `receive_video()`, the JPEG image can be retrieved from this URL.

## Code Style Compliance

The implementation follows the existing code patterns:
- Uses async/await for all commands
- Inherits from `BaseItem`
- Follows the same structure as `Automation` and `Light` items
- Uses proper type hints
- Includes comprehensive docstrings
- Implements event callbacks with `on_status_change()`
- Implements `call_callbacks()` for event dispatching

## Testing

All functionality has been validated:
- ✅ All 32 WHAT commands defined correctly
- ✅ Message formats match OpenWebNet specification
- ✅ Commands with WHERE use NormalMessage
- ✅ Commands without WHERE use GenericMessage
- ✅ Camera class properly inherits from BaseItem
- ✅ WHO is correctly set to VIDEO_DOOR_ENTRY (7)
- ✅ All required methods present and functional
- ✅ Event system properly implemented
- ✅ Unit tests created and passing

## Usage Example

```python
import asyncio
from pyown import Client
from pyown.items import Camera

async def main():
    async with Client("192.168.1.35", 20000) as client:
        camera = Camera(client, "4000")  # Camera 00
        
        # Activate camera
        await camera.receive_video()
        
        # Adjust settings
        await camera.zoom_in()
        await camera.increase_luminosity()
        await camera.increase_contrast()
        
        # Display dial
        await camera.display_dial(1, 1)
        
        # Free resources
        await camera.free_resources()

asyncio.run(main())
```

## Compliance

✅ Follows OpenWebNet WHO=7 specification completely
✅ No HTTP client added (as requested)
✅ Matches existing code style and patterns
✅ Properly documented with examples
✅ Tested and validated
