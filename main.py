import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.logger import Logger

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
        camera_spinner.text = available_cameras[0]
        
        Logger.info(f"Found cameras: {available_cameras}")
    
    def get_selected_camera_index(self):
        """Get the selected camera index from the spinner."""
        if 'camera_spinner' not in self.ids:
            return 0
        camera_text = self.ids.camera_spinner.text
        if camera_text.startswith("Camera "):
            try:
                return int(camera_text.split()[1])
            except (IndexError, ValueError):
                return 0
        return 0
    
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


class MainApp(App):
    """Main Kivy application."""
    
    def build(self):
        """Build the application UI."""
        self.title = 'Posture Tracker'
        Window.size = (800, 600)
        self.root = PostureTrackerApp()
        # Load settings when app starts (give more time for widget initialization)
        Clock.schedule_once(lambda dt: self.root.load_settings(), 0.5)
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
    
    def on_stop(self):
        """Clean up when app is closing."""
        if self.root:
            self.root.stop_tracking()
            self.root.detector.release()
        return True


if __name__ == '__main__':
    MainApp().run()
