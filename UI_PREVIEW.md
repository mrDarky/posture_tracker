# Camera Management UI Preview

## Settings Tab Layout

The Settings tab has been redesigned with two main sections:

### 1. Posture Tracking Settings (Top Section - 25%)
```
┌─────────────────────────────────────────────────────────────┐
│  Tilt Threshold (degrees):  [   15.0   ]                    │
│                                                              │
│  Lower values = stricter posture monitoring                 │
│  Higher values = more lenient monitoring                    │
│  Recommended range: 10-20 degrees                           │
└─────────────────────────────────────────────────────────────┘
```

### 2. Camera Management Section (Middle Section - 45%)
```
┌─────────────────────────────────────────────────────────────┐
│  Camera Management                                           │
│                                                              │
│  [Refresh Camera List]    Status: Found 2 camera(s)         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Scrollable Camera List:                                │ │
│  │                                                        │ │
│  │ ┌──────────────────────────────────────────────────┐  │ │
│  │ │ Camera 0 [Default]                               │  │ │
│  │ │ 640x480 - ✓ Working                              │  │ │
│  │ │          [Test]  [Set Default] (disabled)        │  │ │
│  │ └──────────────────────────────────────────────────┘  │ │
│  │                                                        │ │
│  │ ┌──────────────────────────────────────────────────┐  │ │
│  │ │ Camera 1                                         │  │ │
│  │ │ 1280x720 - ✓ Working                            │  │ │
│  │ │          [Test]  [Set Default]                   │  │ │
│  │ └──────────────────────────────────────────────────┘  │ │
│  │                                                        │ │
│  │ ┌──────────────────────────────────────────────────┐  │ │
│  │ │ Camera 2                                         │  │ │
│  │ │ Failed to read frame - ✗ Not available          │  │ │
│  │ │          [Test] (disabled)  [Set Default] (dis)  │  │ │
│  │ └──────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 3. Save Button and Status (Bottom Section - 15%)
```
┌─────────────────────────────────────────────────────────────┐
│                    [Save Settings]                           │
│                                                              │
│  Settings saved! Threshold: 15.0°                           │
└─────────────────────────────────────────────────────────────┘
```

## Color Coding

- **Green (✓ Working)**: Camera is available and functioning
- **Red (✗ Not available)**: Camera failed to open or read frames
- **[Default] marker**: Indicates the currently selected default camera
- **Disabled buttons**: Grayed out for unavailable cameras or already-default cameras

## User Interactions

### Refresh Camera List Button
- Click to re-scan for available cameras
- Status shows "Scanning..." during detection
- Updates list with newly detected or disconnected cameras

### Test Button (per camera)
- Tests if the camera can capture a frame
- Shows success/failure message in status area
- Useful for verifying camera functionality

### Set Default Button (per camera)
- Sets the camera as the default for the application
- Saves preference to database
- Updates camera dropdown in Camera tab
- Disabled if camera is already default or not working

## Example Status Messages

During refresh:
```
Status: Scanning...
```

After refresh:
```
Status: Found 2 camera(s)
```

After testing Camera 0:
```
Status: Camera 0 test successful!
```

After setting default:
```
Status: Camera 1 set as default
```

## Benefits

1. **Visual Feedback**: Clear indication of which cameras work
2. **Easy Testing**: One-click test for each camera
3. **Flexible Configuration**: Change default camera without code changes
4. **Persistent Settings**: Default camera remembered across restarts
5. **Troubleshooting**: Quickly identify camera issues
