# Posture Tracker

A Python application using Kivy, OpenCV, and MediaPipe to track and monitor your sitting posture in real-time.

## Features

- **Tabbed Interface**: Organized UI with Camera and Settings tabs
- **Light & Dark Theme**: Choose between light and dark appearance modes for comfortable viewing
- **Camera Selection**: Choose from multiple available cameras/devices
- **Real-time Posture Detection**: Uses your webcam to monitor shoulder alignment
- **Visual Feedback**: Displays pose landmarks with dots and lines on video stream
- **Posture Alerts**: Alerts you when your shoulders are tilted beyond a threshold
- **Configurable Threshold**: Set your own tilt angle threshold in the Settings tab
- **Persistent Settings**: Your preferences are saved using SQLite database
- **Start/Stop Controls**: Easy controls to start and stop monitoring

## Requirements

- Python 3.8 or higher
- Webcam
- Operating System: Windows, macOS, or Linux

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mrDarky/posture_tracker.git
cd posture_tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

### Interface Overview

The application features a **tabbed interface** with two main sections:

#### Tab 1: Camera
- **Camera Selection**: Choose from available cameras using the dropdown menu
- **Video Display**: Live camera feed with pose detection overlay
- **Status Indicators**: Real-time tilt angle and posture status
- **Controls**: 
  - **Start Tracking**: Begin posture monitoring
  - **Stop Tracking**: Stop posture monitoring

#### Tab 2: Settings
- **Appearance Theme**: Choose between Dark or Light theme for the application
- **Tilt Threshold**: Configure the angle threshold (default: 15 degrees)
- **Camera Management**: 
  - View all available cameras (USB and built-in)
  - Test camera connections
  - Set default camera
  - Refresh camera list
- **Save Button**: Save your configuration
- **Help Text**: Clear instructions and recommendations

### Controls

- **Camera Dropdown** (Camera Tab): Select which camera/device to use for video capture
- **Start Tracking Button**: Begin posture monitoring with the selected camera
- **Stop Tracking Button**: Stop posture monitoring
- **Theme Dropdown** (Settings Tab): Switch between Dark and Light theme
- **Refresh Camera List** (Settings Tab): Re-scan for available cameras
- **Test Button** (Settings Tab): Test a specific camera's connection
- **Set Default Button** (Settings Tab): Set a camera as the default for the application

### How It Works

1. The app uses MediaPipe Pose to detect body landmarks from your webcam
2. It tracks your left and right shoulders
3. Calculates the tilt angle between shoulders
4. If the tilt exceeds the threshold, it displays "Bad Posture!" in red
5. Visual feedback includes:
   - Green dots on shoulders
   - Green line connecting shoulders
   - Full body pose skeleton
   - Real-time tilt angle display

## Settings

- **Theme**: Choose between Dark (default) and Light appearance modes
  - Dark theme: Comfortable for low-light environments with light text on dark backgrounds
  - Light theme: Ideal for bright environments with dark text on light backgrounds
  - All text has proper contrast for readability in both themes
  - Theme preference is saved and persists across sessions

- **Tilt Threshold**: The angle (in degrees) at which the app considers your posture bad
  - Default: 15.0 degrees
  - Range: 0-90 degrees
  - Lower values = more strict posture monitoring
  - Higher values = more lenient posture monitoring

Settings are automatically saved to `posture_settings.db` and persist across sessions.

## Troubleshooting

### Common Startup Messages

You may see some informational messages when starting the application. These are normal and can be safely ignored:

- **MediaPipe Feedback Manager Warnings**: "Feedback manager requires a model with a single signature inference..." - This is an informational message from MediaPipe and does not affect functionality.
- **MTD Input Device Warnings**: "[WARNING] [MTD] Unable to open device..." - This is a Kivy multitouch device warning. The application is configured to work without multitouch devices.
- **Camera Detection Messages**: During startup, the app scans for available cameras which may produce brief messages. This is normal.

### Camera Issues

- **No cameras detected**: Make sure your webcam is connected and not being used by another application
- **Permission errors**: On Linux, you may need to add your user to the `video` group: `sudo usermod -a -G video $USER`
- **Camera not working**: Try a different camera from the Settings tab or restart the application

## Project Structure

- `main.py`: Main application entry point and Kivy UI logic
- `posture_detector.py`: Posture detection using MediaPipe
- `database.py`: SQLite database for settings persistence
- `posture_tracker.kv`: Kivy UI layout definition
- `requirements.txt`: Python dependencies

## Dependencies

- **Kivy**: UI framework
- **OpenCV**: Video capture and image processing
- **MediaPipe**: Pose detection and landmark tracking
- **NumPy**: Numerical computations
- **Pillow**: Image processing support

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.