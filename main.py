import os
import warnings

# Suppress warnings before importing other modules
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['KIVY_NO_CONSOLELOG'] = '0'
# Suppress OpenCV warnings
os.environ['OPENCV_LOG_LEVEL'] = 'ERROR'
os.environ['OPENCV_VIDEOIO_DEBUG'] = '0'
warnings.filterwarnings('ignore', category=UserWarning, module='google.protobuf')
warnings.filterwarnings('ignore', category=FutureWarning, module='mediapipe')

import cv2
# Set OpenCV log level to ERROR only (suppresses WARN messages)
# Only available in OpenCV 4.x
try:
    cv2.setLogLevel(3)
except AttributeError:
    pass  # setLogLevel not available in this OpenCV version
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.config import Config

# Configure Kivy to not require multitouch input device
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from database import SettingsDatabase
from posture_detector import PostureDetector


# UI Color constants
NEUTRAL_COLOR = (0.5, 0.5, 0.5, 1)
GOOD_COLOR = (0, 1, 0, 1)
BAD_COLOR = (1, 0, 0, 1)


class PostureTrackerApp(TabbedPanel):
    """Main application layout with tabs."""
    
    # Constants for widget initialization
    WIDGET_INIT_RETRY_DELAY = 0.2  # seconds
    MAX_WIDGET_INIT_RETRIES = 25  # max 5 seconds (25 * 0.2)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = SettingsDatabase()
        self.detector = PostureDetector()
        self.capture = None
        self.is_tracking = False
        self.event = None
        self._camera_list_retry_count = 0
        self._settings_load_retry_count = 0
        
        # Populate camera list after UI is built (give more time for widget initialization)
        Clock.schedule_once(self.populate_camera_list, 0.5)
    
    def populate_camera_list(self, dt):
        """Populate the camera selection spinner with available cameras."""
        # Check if camera_spinner is available in ids
        if 'camera_spinner' not in self.ids:
            # Reschedule if not ready yet (max 50 retries = 5 seconds)
            self._camera_list_retry_count += 1
            if self._camera_list_retry_count < 50:
                # Only log at specific intervals to reduce noise
                if self._camera_list_retry_count == 1 or self._camera_list_retry_count % 10 == 0:
                    Logger.debug(f"camera_spinner not yet available, retry {self._camera_list_retry_count}/50")
                Clock.schedule_once(self.populate_camera_list, 0.1)
            else:
                Logger.error("Camera spinner not available after 5 seconds")
            return
        
        camera_spinner = self.ids.camera_spinner
        available_cameras = []
        
        # Try to detect available cameras (check indices 0-2, reduced for faster startup)
        for i in range(3):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(f"Camera {i}")
                cap.release()
        
        if not available_cameras:
            available_cameras = ["No cameras found"]
        
        camera_spinner.values = available_cameras
        
        # Set default camera from database
        default_camera = self.db.get_default_camera()
        if f"Camera {default_camera}" in available_cameras:
            camera_spinner.text = f"Camera {default_camera}"
        else:
            camera_spinner.text = available_cameras[0]
        
        Logger.info(f"Found cameras: {available_cameras}")
    
    def get_selected_camera_index(self):
        """Get the selected camera index from the spinner."""
        if 'camera_spinner' not in self.ids:
            return self.db.get_default_camera()
        camera_text = self.ids.camera_spinner.text
        if camera_text.startswith("Camera "):
            try:
                return int(camera_text.split()[1])
            except (IndexError, ValueError):
                return self.db.get_default_camera()
        return self.db.get_default_camera()
    
    def start_tracking(self):
        """Start video capture and posture tracking."""
        if not self.is_tracking:
            # Get selected camera index
            camera_index = self.get_selected_camera_index()
            
            # Open camera
            self.capture = cv2.VideoCapture(camera_index)
            
            if not self.capture.isOpened():
                Logger.error(f"Failed to open camera {camera_index}")
                return
            
            self.is_tracking = True
            self.ids.start_button.disabled = True
            self.ids.stop_button.disabled = False
            if 'camera_spinner' in self.ids:
                self.ids.camera_spinner.disabled = True
            
            # Schedule frame update
            self.event = Clock.schedule_interval(self.update_frame, 1.0/30.0)
            Logger.info(f"Tracking started with camera {camera_index}")
    
    def stop_tracking(self):
        """Stop video capture and posture tracking."""
        if self.is_tracking:
            self.is_tracking = False
            
            # Stop scheduled updates
            if self.event:
                self.event.cancel()
                self.event = None
            
            # Release camera
            if self.capture:
                self.capture.release()
                self.capture = None
            
            # Clear display
            self.ids.camera_display.texture = None
            self.ids.tilt_label.text = '0.0°'
            self.ids.status_label.text = 'Stopped'
            self.ids.status_label.color = NEUTRAL_COLOR
            
            self.ids.start_button.disabled = False
            self.ids.stop_button.disabled = True
            if 'camera_spinner' in self.ids:
                self.ids.camera_spinner.disabled = False
            Logger.info("Tracking stopped")
    
    def update_frame(self, dt):
        """Update video frame and detect posture."""
        if not self.is_tracking or not self.capture:
            return
        
        ret, frame = self.capture.read()
        
        if not ret:
            Logger.error("Failed to read frame")
            return
        
        # Process frame for posture detection
        processed_frame, tilt_angle, left_shoulder, right_shoulder = self.detector.process_frame(frame)
        
        # Get threshold from database
        threshold = self.db.get_tilt_threshold()
        
        # Check if posture is bad
        is_bad_posture = tilt_angle > threshold
        
        # Update UI
        self.ids.tilt_label.text = f'{tilt_angle:.1f}°'
        
        if is_bad_posture:
            self.ids.status_label.text = 'Bad Posture!'
            self.ids.status_label.color = BAD_COLOR
            self.ids.tilt_label.color = BAD_COLOR
        else:
            self.ids.status_label.text = 'Good Posture'
            self.ids.status_label.color = GOOD_COLOR
            self.ids.tilt_label.color = GOOD_COLOR
        
        # Display threshold on frame
        cv2.putText(processed_frame, f'Threshold: {threshold:.1f}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(processed_frame, f'Tilt: {tilt_angle:.1f}', (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Convert to texture and display
        buf = cv2.flip(processed_frame, 0).tobytes()
        texture = Texture.create(size=(processed_frame.shape[1], processed_frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.ids.camera_display.texture = texture
    
    def validate_threshold(self, value):
        """Validate and clamp threshold value to valid range (0-90 degrees)."""
        if value < 0:
            return 0
        if value > 90:
            return 90
        return value
    
    def save_settings(self):
        """Save settings from the settings tab."""
        # Check if threshold_input is available
        if 'threshold_input' not in self.ids or 'settings_status' not in self.ids:
            Logger.warning("Settings widgets not yet available")
            return
        
        try:
            threshold = float(self.ids.threshold_input.text)
            threshold = self.validate_threshold(threshold)
            self.db.set_tilt_threshold(threshold)
            self.ids.settings_status.text = f'Settings saved! Threshold: {threshold}°'
            self.ids.settings_status.color = GOOD_COLOR
            Logger.info(f"Settings saved: threshold={threshold}")
        except ValueError:
            self.ids.settings_status.text = 'Error: Invalid threshold value'
            self.ids.settings_status.color = BAD_COLOR
            Logger.error("Invalid threshold value")
    
    def load_settings(self):
        """Load current settings into the settings tab."""
        # Check if threshold_input is available
        if 'threshold_input' not in self.ids:
            # Retry loading settings after a short delay (with max retry limit)
            self._settings_load_retry_count += 1
            if self._settings_load_retry_count < self.MAX_WIDGET_INIT_RETRIES:
                # Only log at specific intervals to reduce noise
                if self._settings_load_retry_count == 1 or self._settings_load_retry_count % 10 == 0:
                    Logger.debug(f"threshold_input not yet available, retry {self._settings_load_retry_count}/{self.MAX_WIDGET_INIT_RETRIES}")
                Clock.schedule_once(lambda dt: self.load_settings(), self.WIDGET_INIT_RETRY_DELAY)
            else:
                Logger.error("threshold_input not available after maximum retries")
            return
        
        # Reset retry counter on success
        self._settings_load_retry_count = 0
        
        threshold = self.db.get_tilt_threshold()
        self.ids.threshold_input.text = str(threshold)
        if 'settings_status' in self.ids:
            self.ids.settings_status.text = ''
    
    def detect_cameras(self, max_cameras=10):
        """
        Detect available cameras and return information about them.
        
        Args:
            max_cameras: Maximum number of camera indices to check (default: 10).
                        Most systems have 0-2 cameras, but checking up to 10 covers
                        edge cases with multiple USB cameras or virtual cameras.
        
        Returns:
            List of dicts with camera info: [{'index': 0, 'name': 'Camera 0', 'available': True, 'info': '...'}]
        """
        cameras = []
        
        for i in range(max_cameras):
            cap = cv2.VideoCapture(i)
            
            if cap.isOpened():
                # Try to get camera properties
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                
                # Try to read a frame to verify it's working
                ret, frame = cap.read()
                
                camera_info = {
                    'index': i,
                    'name': f'Camera {i}',
                    'available': ret,
                    'info': f'{int(width)}x{int(height)}' if ret else 'Failed to read frame'
                }
                cameras.append(camera_info)
                cap.release()
            
        return cameras
    
    def refresh_camera_list(self):
        """Refresh the camera list in the settings tab."""
        if 'camera_list_container' not in self.ids:
            Logger.warning("camera_list_container not yet available")
            return
        
        if 'camera_scan_status' in self.ids:
            self.ids.camera_scan_status.text = 'Scanning...'
            self.ids.camera_scan_status.color = (1, 1, 0, 1)  # Yellow
        
        # Run camera detection (this might take a moment)
        Clock.schedule_once(lambda dt: self._update_camera_list(), 0.1)
    
    def _update_camera_list(self):
        """Update the camera list UI with detected cameras."""
        cameras = self.detect_cameras()
        
        # Clear existing camera list
        container = self.ids.camera_list_container
        container.clear_widgets()
        
        if not cameras:
            no_camera_label = Label(
                text='No cameras detected',
                size_hint_y=None,
                height=40,
                color=(1, 0, 0, 1)
            )
            container.add_widget(no_camera_label)
        else:
            default_camera = self.db.get_default_camera()
            
            for cam in cameras:
                # Create a horizontal box for each camera
                cam_box = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=60,
                    spacing=5,
                    padding=[5, 5]
                )
                
                # Camera info label
                status_color = GOOD_COLOR if cam['available'] else BAD_COLOR
                status_text = '✓ Working' if cam['available'] else '✗ Not available'
                is_default = ' [Default]' if cam['index'] == default_camera else ''
                
                info_label = Label(
                    text=f"{cam['name']}{is_default}\n{cam['info']} - {status_text}",
                    size_hint_x=0.5,
                    color=status_color,
                    halign='left',
                    valign='middle'
                )
                info_label.bind(size=info_label.setter('text_size'))
                
                # Test button
                test_btn = Button(
                    text='Test',
                    size_hint_x=0.25,
                    disabled=not cam['available'],
                    background_color=(0.3, 0.6, 0.9, 1)
                )
                test_btn.bind(on_press=lambda btn, idx=cam['index']: self.test_camera(idx))
                
                # Set as default button
                default_btn = Button(
                    text='Set Default',
                    size_hint_x=0.25,
                    disabled=not cam['available'] or cam['index'] == default_camera,
                    background_color=(0, 0.7, 0.3, 1)
                )
                default_btn.bind(on_press=lambda btn, idx=cam['index']: self.set_default_camera(idx))
                
                cam_box.add_widget(info_label)
                cam_box.add_widget(test_btn)
                cam_box.add_widget(default_btn)
                
                container.add_widget(cam_box)
        
        if 'camera_scan_status' in self.ids:
            self.ids.camera_scan_status.text = f'Found {len(cameras)} camera(s)'
            self.ids.camera_scan_status.color = GOOD_COLOR if cameras else BAD_COLOR
    
    def test_camera(self, camera_index):
        """Test a camera by trying to capture a frame."""
        if 'camera_scan_status' in self.ids:
            self.ids.camera_scan_status.text = f'Testing Camera {camera_index}...'
            self.ids.camera_scan_status.color = (1, 1, 0, 1)  # Yellow
        
        cap = cv2.VideoCapture(camera_index)
        
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                if 'camera_scan_status' in self.ids:
                    self.ids.camera_scan_status.text = f'Camera {camera_index} test successful!'
                    self.ids.camera_scan_status.color = GOOD_COLOR
                Logger.info(f"Camera {camera_index} test successful")
            else:
                if 'camera_scan_status' in self.ids:
                    self.ids.camera_scan_status.text = f'Camera {camera_index} failed to capture frame'
                    self.ids.camera_scan_status.color = BAD_COLOR
                Logger.error(f"Camera {camera_index} failed to capture frame")
        else:
            if 'camera_scan_status' in self.ids:
                self.ids.camera_scan_status.text = f'Camera {camera_index} could not be opened'
                self.ids.camera_scan_status.color = BAD_COLOR
            Logger.error(f"Camera {camera_index} could not be opened")
    
    def set_default_camera(self, camera_index):
        """Set the default camera for the application."""
        self.db.set_default_camera(camera_index)
        
        if 'camera_scan_status' in self.ids:
            self.ids.camera_scan_status.text = f'Camera {camera_index} set as default'
            self.ids.camera_scan_status.color = GOOD_COLOR
        
        Logger.info(f"Default camera set to {camera_index}")
        
        # Update the camera spinner in the Camera tab
        if 'camera_spinner' in self.ids:
            self.ids.camera_spinner.text = f"Camera {camera_index}"
        
        # Refresh the camera list to update the UI
        Clock.schedule_once(lambda dt: self._update_camera_list(), 0.5)


class MainApp(App):
    """Main Kivy application."""
    
    def build(self):
        """Build the application UI."""
        self.title = 'Posture Tracker'
        Window.size = (800, 600)
        self.root = PostureTrackerApp()
        # Load settings when app starts (give more time for widget initialization)
        Clock.schedule_once(lambda dt: self.root.load_settings(), 0.5)
        # Populate camera list in settings tab
        Clock.schedule_once(lambda dt: self.root.refresh_camera_list(), 1.0)
        return self.root
    
    def start_tracking(self):
        """Start tracking from button."""
        self.root.start_tracking()
    
    def stop_tracking(self):
        """Stop tracking from button."""
        self.root.stop_tracking()
    
    def save_settings(self):
        """Save settings from button."""
        self.root.save_settings()
    
    def refresh_camera_list(self):
        """Refresh camera list from button."""
        self.root.refresh_camera_list()
    
    def on_stop(self):
        """Clean up when app is closing."""
        if self.root:
            self.root.stop_tracking()
            self.root.detector.release()
        return True


if __name__ == '__main__':
    MainApp().run()
