# Posture Tracker - Architecture

## System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                         (Kivy - main.py)                        │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐                │
│  │  Start   │  │   Stop   │  │   Settings   │                │
│  │  Button  │  │  Button  │  │    Button    │                │
│  └─────┬────┘  └─────┬────┘  └──────┬───────┘                │
│        │             │               │                          │
│        v             v               v                          │
│  ┌─────────────────────────────────────────────────┐          │
│  │         Camera Display (Video Stream)            │          │
│  │                                                   │          │
│  │    • Shows live video with pose landmarks        │          │
│  │    • Green dots on shoulders                     │          │
│  │    • Green line between shoulders                │          │
│  │    • Full body skeleton overlay                  │          │
│  │    • Current tilt angle display                  │          │
│  │    • Status: "Good Posture" / "Bad Posture!"    │          │
│  └─────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                          │
                          v
┌─────────────────────────────────────────────────────────────────┐
│                     POSTURE DETECTOR                            │
│                  (posture_detector.py)                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    MediaPipe Pose                         │ │
│  │                                                           │ │
│  │  1. Capture video frame from camera                      │ │
│  │  2. Detect 33 body landmarks                             │ │
│  │  3. Extract left shoulder (landmark #11)                 │ │
│  │  4. Extract right shoulder (landmark #12)                │ │
│  │  5. Calculate tilt angle between shoulders               │ │
│  │                                                           │ │
│  │     angle = abs(arctan2(y_diff, x_diff) * 180/π)        │ │
│  │                                                           │ │
│  │  6. Draw landmarks and connections on frame              │ │
│  │  7. Return: processed_frame, tilt_angle                  │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                          │
                          v
┌─────────────────────────────────────────────────────────────────┐
│                    POSTURE EVALUATION                           │
│                     (main.py logic)                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  if tilt_angle > threshold:                              │ │
│  │      status = "Bad Posture!"                             │ │
│  │      color = RED                                         │ │
│  │  else:                                                   │ │
│  │      status = "Good Posture"                             │ │
│  │      color = GREEN                                       │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                          │
                          v
┌─────────────────────────────────────────────────────────────────┐
│                   SETTINGS MANAGEMENT                           │
│                     (database.py)                               │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                 SQLite Database                           │ │
│  │              (posture_settings.db)                        │ │
│  │                                                           │ │
│  │  Table: settings                                         │ │
│  │  ┌──────────────────┬──────────────────┐                │ │
│  │  │      key         │      value       │                │ │
│  │  ├──────────────────┼──────────────────┤                │ │
│  │  │ tilt_threshold   │      15.0        │                │ │
│  │  └──────────────────┴──────────────────┘                │ │
│  │                                                           │ │
│  │  • get_tilt_threshold() → reads value                   │ │
│  │  • set_tilt_threshold(n) → saves value                  │ │
│  │  • Persists across app sessions                         │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### 1. main.py (Kivy Application)
- **UI Management**: Handles all user interface elements
- **Video Streaming**: Updates camera display at 30 FPS
- **Button Controls**: Start/Stop monitoring, open settings
- **Status Display**: Shows tilt angle and posture status
- **Color Feedback**: Green (good) / Red (bad) visual alerts

### 2. posture_detector.py (Pose Detection)
- **MediaPipe Integration**: Initializes pose detection model
- **Landmark Detection**: Identifies 33 body points
- **Shoulder Tracking**: Focuses on left/right shoulder landmarks
- **Angle Calculation**: Computes tilt from shoulder positions
- **Visual Overlay**: Draws skeleton, dots, and lines on video

### 3. database.py (Settings Persistence)
- **SQLite Operations**: CREATE, INSERT, SELECT operations
- **Threshold Storage**: Saves user's preferred tilt threshold
- **Session Persistence**: Remembers settings across app restarts
- **Default Values**: Provides fallback values (15.0°)

### 4. posture_tracker.kv (UI Layout)
- **Layout Definition**: Kivy language markup
- **Widget Hierarchy**: Buttons, labels, image display
- **Settings Dialog**: Popup for threshold configuration
- **Responsive Design**: Adapts to window size

## Data Flow

```
Camera → OpenCV → MediaPipe → Shoulder Positions → Tilt Angle
                                                        ↓
                                                   Compare with
                                                    Threshold
                                                        ↓
                                            ┌───────────┴──────────┐
                                            ↓                      ↓
                                      Good Posture          Bad Posture
                                      (Green Alert)         (Red Alert)
```

## Key Algorithms

### Shoulder Tilt Calculation
```python
# Given two shoulder points (x1, y1) and (x2, y2)
x_diff = x2 - x1
y_diff = y2 - y1

# Calculate angle from horizontal
angle_radians = atan2(y_diff, x_diff)
angle_degrees = abs(angle_radians * 180 / π)

# 0° = level shoulders
# Higher values = more tilt
```

### Posture Evaluation
```python
is_bad_posture = (tilt_angle > threshold)

if is_bad_posture:
    display_color = RED
    display_text = "Bad Posture!"
else:
    display_color = GREEN
    display_text = "Good Posture"
```

## Dependencies Graph

```
main.py
  ├── kivy (UI framework)
  ├── opencv (cv2 - video capture)
  ├── posture_detector.py
  │     ├── mediapipe (pose detection)
  │     ├── opencv (cv2 - image processing)
  │     └── numpy (calculations)
  └── database.py
        └── sqlite3 (settings storage)
```

## Execution Sequence

1. **App Start**
   - Load Kivy UI
   - Initialize database connection
   - Initialize MediaPipe pose detector
   - Load saved threshold from database

2. **User Clicks "Start"**
   - Open camera (cv2.VideoCapture)
   - Schedule frame updates (30 FPS)
   - Enable "Stop" button, disable "Start" button

3. **Each Frame (every 33ms)**
   - Capture frame from camera
   - Process with MediaPipe pose detector
   - Extract shoulder landmarks
   - Calculate tilt angle
   - Compare with threshold
   - Update UI display
   - Draw visual feedback on frame

4. **User Clicks "Settings"**
   - Open settings dialog
   - Display current threshold
   - Allow user to modify value
   - Save to database on confirm

5. **User Clicks "Stop"**
   - Cancel frame updates
   - Release camera
   - Clear display
   - Enable "Start" button, disable "Stop" button

6. **App Close**
   - Stop any active monitoring
   - Release camera resources
   - Close database connection
   - Release MediaPipe resources

## Performance Considerations

- **Frame Rate**: 30 FPS provides smooth video
- **Pose Detection**: ~20-40ms per frame on modern CPU
- **Database**: Minimal overhead (only on settings change)
- **Memory**: MediaPipe models loaded once at startup
- **CPU Usage**: Higher during active monitoring

## Error Handling

- Camera not available → Display error message
- No pose detected → Show 0° tilt, no alert
- Invalid threshold → Clamp to valid range (0-90°)
- Database errors → Use default values
