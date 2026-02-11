# Posture Tracker

A Python application using Kivy, OpenCV, and MediaPipe to track and monitor your sitting posture in real-time.

## Features

- **Real-time Posture Detection**: Uses your webcam to monitor shoulder alignment
- **Visual Feedback**: Displays pose landmarks with dots and lines on video stream
- **Posture Alerts**: Alerts you when your shoulders are tilted beyond a threshold
- **Configurable Threshold**: Set your own tilt angle threshold in settings
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

### Controls

- **Start Button**: Begin posture monitoring
- **Stop Button**: Stop posture monitoring
- **Settings Button**: Configure tilt threshold (default: 15 degrees)

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

- **Tilt Threshold**: The angle (in degrees) at which the app considers your posture bad
  - Default: 15.0 degrees
  - Range: 0-90 degrees
  - Lower values = more strict posture monitoring
  - Higher values = more lenient posture monitoring

Settings are automatically saved to `posture_settings.db` and persist across sessions.

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