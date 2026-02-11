import cv2
import mediapipe as mp
import numpy as np
import math
import os
import warnings

# Suppress TensorFlow/MediaPipe warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore', category=UserWarning, module='google.protobuf')
warnings.filterwarnings('ignore', category=FutureWarning, module='mediapipe')


class PostureDetector:
    """Posture detection using MediaPipe Pose."""
    
    def __init__(self):
        """Initialize MediaPipe Pose solution."""
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def calculate_tilt(self, left_shoulder, right_shoulder):
        """Calculate shoulder tilt angle."""
        if left_shoulder is None or right_shoulder is None:
            return 0
        
        x_diff = right_shoulder[0] - left_shoulder[0]
        y_diff = right_shoulder[1] - left_shoulder[1]
        
        # Calculate angle from horizontal (0 degrees means level shoulders)
        angle = math.degrees(math.atan2(y_diff, x_diff))
        return abs(angle)
    
    def process_frame(self, frame):
        """
        Process a video frame for posture detection.
        
        Returns:
            processed_frame: Frame with pose landmarks drawn
            tilt_angle: Shoulder tilt angle in degrees
            is_bad_posture: Boolean indicating if posture is bad
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.pose.process(rgb_frame)
        
        tilt_angle = 0
        left_shoulder = None
        right_shoulder = None
        
        if results.pose_landmarks:
            # Draw pose landmarks on the frame
            self.mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            # Get shoulder positions
            landmarks = results.pose_landmarks.landmark
            h, w, c = frame.shape
            
            # Left shoulder (landmark 11)
            left_shoulder_lm = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            left_shoulder = (int(left_shoulder_lm.x * w), int(left_shoulder_lm.y * h))
            
            # Right shoulder (landmark 12)
            right_shoulder_lm = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            right_shoulder = (int(right_shoulder_lm.x * w), int(right_shoulder_lm.y * h))
            
            # Calculate tilt angle
            tilt_angle = self.calculate_tilt(left_shoulder, right_shoulder)
            
            # Draw line between shoulders
            cv2.line(frame, left_shoulder, right_shoulder, (0, 255, 0), 2)
            
            # Draw shoulder points
            cv2.circle(frame, left_shoulder, 5, (0, 0, 255), -1)
            cv2.circle(frame, right_shoulder, 5, (0, 0, 255), -1)
        
        return frame, tilt_angle, left_shoulder, right_shoulder
    
    def release(self):
        """Release MediaPipe resources."""
        self.pose.close()
