import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.logger import Logger

from database import SettingsDatabase
from posture_detector import PostureDetector


class SettingsPopup(Popup):
    """Popup window for configuring settings."""
    
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        # Load current threshold
        threshold = self.db.get_tilt_threshold()
        self.ids.threshold_input.text = str(threshold)
    
    def save_settings(self):
        """Save settings to database and close popup."""
        try:
            threshold = float(self.ids.threshold_input.text)
            if threshold < 0:
                threshold = 0
            if threshold > 90:
                threshold = 90
            self.db.set_tilt_threshold(threshold)
            Logger.info(f"Settings saved: threshold={threshold}")
            self.dismiss()
        except ValueError:
            Logger.error("Invalid threshold value")


class PostureTrackerApp(BoxLayout):
    """Main application layout."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = SettingsDatabase()
        self.detector = PostureDetector()
        self.capture = None
        self.is_tracking = False
        self.event = None
    
    def start_tracking(self):
        """Start video capture and posture tracking."""
        if not self.is_tracking:
            # Open camera
            self.capture = cv2.VideoCapture(0)
            
            if not self.capture.isOpened():
                Logger.error("Failed to open camera")
                return
            
            self.is_tracking = True
            self.ids.start_button.disabled = True
            self.ids.stop_button.disabled = False
            
            # Schedule frame update
            self.event = Clock.schedule_interval(self.update_frame, 1.0/30.0)
            Logger.info("Tracking started")
    
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
            self.ids.status_label.color = (0.5, 0.5, 0.5, 1)
            
            self.ids.start_button.disabled = False
            self.ids.stop_button.disabled = True
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
            self.ids.status_label.color = (1, 0, 0, 1)
            self.ids.tilt_label.color = (1, 0, 0, 1)
        else:
            self.ids.status_label.text = 'Good Posture'
            self.ids.status_label.color = (0, 1, 0, 1)
            self.ids.tilt_label.color = (0, 1, 0, 1)
        
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


class MainApp(App):
    """Main Kivy application."""
    
    def build(self):
        """Build the application UI."""
        self.title = 'Posture Tracker'
        Window.size = (800, 600)
        self.root = PostureTrackerApp()
        return self.root
    
    def start_tracking(self):
        """Start tracking from button."""
        self.root.start_tracking()
    
    def stop_tracking(self):
        """Stop tracking from button."""
        self.root.stop_tracking()
    
    def show_settings(self):
        """Show settings popup."""
        popup = SettingsPopup(self.root.db)
        popup.open()
    
    def on_stop(self):
        """Clean up when app is closing."""
        if self.root:
            self.root.stop_tracking()
            self.root.detector.release()
        return True


if __name__ == '__main__':
    MainApp().run()
