# Posture Tracker

A Python application using Kivy, OpenCV, and MediaPipe to track and monitor your sitting posture in real-time, with an integrated training module for exercise form checking.

## Features

### Posture Tracking
- **Tabbed Interface**: Organized UI with Camera, Training, and Settings tabs
- **Light & Dark Theme**: Choose between light and dark appearance modes for comfortable viewing
- **Camera Selection**: Choose from multiple available cameras/devices
- **Real-time Posture Detection**: Uses your webcam to monitor shoulder alignment
- **Visual Feedback**: Displays pose landmarks with dots and lines on video stream
- **Posture Alerts**: Alerts you when your shoulders are tilted beyond a threshold
- **Configurable Threshold**: Set your own tilt angle threshold in the Settings tab
- **Persistent Settings**: Your preferences are saved using SQLite database
- **Start/Stop Controls**: Easy controls to start and stop monitoring

### Training Module (NEW!)
- **24+ Exercise Library**: Comprehensive database of exercises including:
  - **Bodyweight exercises**: Push-ups, Pull-ups, Squats, Lunges, Planks, Burpees, Mountain Climbers, Dips
  - **Dumbbell exercises**: Shoulder Press, Bicep Curls, Bent-Over Rows, Goblet Squats, Lunges, Deadlifts, Chest Press, Lateral Raises, Tricep Extensions, Arnold Press
  - **Stretching exercises**: Hamstring Stretch, Quad Stretch, Chest Doorway Stretch, Shoulder Stretch, Cat-Cow Stretch, Hip Flexor Stretch
- **Exercise Categories**: Filter exercises by Bodyweight, Dumbbells, or Stretching
- **Real-time Form Checking**: Camera-based validation of exercise technique
- **Rep Counter**: Automatic counting for supported exercises (push-ups, squats, etc.)
- **Visual Feedback**: Live feedback on form and technique
- **Workout Builder**: 
  - Add exercises to your current workout
  - Remove exercises from workout
  - Clear entire workout
  - View all exercises in your workout plan
- **Exercise Details**: View instructions, target muscles, and difficulty level for each exercise

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

The application features a **tabbed interface** with three main sections:

#### Tab 1: Camera
- **Camera Selection**: Choose from available cameras using the dropdown menu
- **Video Display**: Live camera feed with pose detection overlay
- **Status Indicators**: Real-time tilt angle and posture status
- **Controls**: 
  - **Start Tracking**: Begin posture monitoring
  - **Stop Tracking**: Stop posture monitoring

#### Tab 2: Training (NEW!)
- **Exercise Selection**: Choose from 24+ exercises across multiple categories
- **Category Filter**: Filter exercises by Bodyweight, Dumbbells, or Stretching
- **Live Camera Feed**: Real-time video with pose detection and form checking
- **Rep Counter**: Automatic counting for supported exercises
- **Form Feedback**: Real-time feedback on exercise technique
- **Exercise Information**: 
  - Exercise name, category, and difficulty level
  - Description and target muscles
  - Step-by-step instructions
- **Workout Builder**:
  - Add current exercise to workout with + button
  - View all exercises in current workout
  - Remove exercises from workout
  - Clear entire workout
- **Controls**:
  - **Start Exercise**: Begin exercise with camera tracking
  - **Stop Exercise**: Stop exercise tracking
  - **Reset**: Reset rep counter

#### Tab 3: Settings
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

#### Camera Tab
- **Camera Dropdown**: Select which camera/device to use for video capture
- **Start Tracking Button**: Begin posture monitoring with the selected camera
- **Stop Tracking Button**: Stop posture monitoring

#### Training Tab
- **Exercise Dropdown**: Select an exercise from the library
- **Category Filter Dropdown**: Filter exercises by category (All, Bodyweight, Dumbbells, Stretching)
- **Start Exercise Button**: Begin exercise with camera-based form checking
- **Stop Exercise Button**: Stop exercise tracking
- **Reset Button**: Reset the rep counter
- **+ Button**: Add current exercise to your workout
- **Clear Button**: Clear all exercises from current workout
- **✕ Button** (on workout items): Remove specific exercise from workout

#### Settings Tab
- **Theme Dropdown**: Switch between Dark and Light theme
- **Refresh Camera List**: Re-scan for available cameras
- **Test Button**: Test a specific camera's connection
- **Set Default Button**: Set a camera as the default for the application

### How It Works

#### Posture Tracking
1. The app uses MediaPipe Pose to detect body landmarks from your webcam
2. It tracks your left and right shoulders
3. Calculates the tilt angle between shoulders
4. If the tilt exceeds the threshold, it displays "Bad Posture!" in red
5. Visual feedback includes:
   - Green dots on shoulders
   - Green line connecting shoulders
   - Full body pose skeleton
   - Real-time tilt angle display

#### Training Module
1. **Exercise Selection**: Choose from the exercise library or filter by category
2. **Start Exercise**: Click "Start Exercise" to begin camera-based form checking
3. **Real-time Feedback**: The app provides:
   - Automatic rep counting for supported exercises (push-ups, squats, pull-ups)
   - Live form feedback (e.g., "Keep body straight", "Go deeper")
   - Visual pose overlay showing your body position
4. **Form Checking**: The app analyzes your body angles and positions to validate:
   - Push-ups: Elbow angle, body alignment, depth
   - Squats: Knee angle, back position, depth
   - Planks: Body alignment, hip position
   - General exercises: Pose visibility and positioning
5. **Workout Building**: Add exercises to create a custom workout routine

## Exercise Library

The app includes 24+ exercises across three categories:

### Bodyweight Exercises (8)
- **Push-ups**: Classic upper body exercise
- **Pull-ups**: Upper body pulling exercise (Intermediate)
- **Squats**: Fundamental lower body exercise
- **Lunges**: Single-leg exercise for legs and balance
- **Plank**: Isometric core strengthening
- **Burpees**: Full body cardio exercise (Intermediate)
- **Mountain Climbers**: Dynamic core and cardio
- **Dips**: Upper body triceps and chest (Intermediate)

### Dumbbell Exercises (10)
- **Dumbbell Shoulder Press**: Overhead pressing for shoulders
- **Dumbbell Bicep Curl**: Isolation for biceps
- **Dumbbell Bent-Over Row**: Back exercise (Intermediate)
- **Goblet Squat**: Squat variation with dumbbell
- **Dumbbell Lunges**: Weighted lunge (Intermediate)
- **Dumbbell Deadlift**: Hip hinge for posterior chain (Intermediate)
- **Dumbbell Chest Press**: Chest pressing on bench
- **Lateral Raises**: Shoulder isolation
- **Overhead Tricep Extension**: Triceps isolation
- **Arnold Press**: Rotational shoulder press (Advanced)

### Stretching Exercises (6)
- **Hamstring Stretch**: Stretches back of thighs
- **Quadriceps Stretch**: Stretches front of thigh
- **Chest Doorway Stretch**: Opens chest and shoulders
- **Cross-Body Shoulder Stretch**: Shoulder and upper back
- **Cat-Cow Stretch**: Dynamic spine mobility
- **Hip Flexor Stretch**: Stretches front of hip

Each exercise includes:
- Difficulty level (Beginner, Intermediate, Advanced)
- Target muscle groups
- Step-by-step instructions
- Form checking criteria (where applicable)

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
- `exercise_database.py`: Exercise library with 24+ exercises
- `exercise_detector.py`: Exercise form checking and rep counting
- `database.py`: SQLite database for settings and workout persistence
- `posture_tracker.kv`: Kivy UI layout definition
- `requirements.txt`: Python dependencies
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