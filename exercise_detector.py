"""
Exercise detector for checking exercise form using MediaPipe pose detection.
Provides real-time feedback on exercise technique.
"""

import cv2
import numpy as np
import math
from posture_detector import PostureDetector


class ExerciseDetector:
    """Detects and validates exercise form using pose landmarks."""
    
    def __init__(self):
        """Initialize exercise detector with pose detection."""
        self.posture_detector = PostureDetector()
        self.mp_pose = self.posture_detector.mp_pose
        self.current_exercise = None
        self.rep_count = 0
        self.last_state = None
        
    def calculate_angle(self, point1, point2, point3):
        """
        Calculate angle between three points.
        
        Args:
            point1, point2, point3: Tuples of (x, y) coordinates
            
        Returns:
            Angle in degrees
        """
        if None in [point1, point2, point3]:
            return 0
            
        # Calculate vectors
        vector1 = np.array([point1[0] - point2[0], point1[1] - point2[1]])
        vector2 = np.array([point3[0] - point2[0], point3[1] - point2[1]])
        
        # Calculate angle
        cosine = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
        cosine = np.clip(cosine, -1.0, 1.0)
        angle = math.degrees(math.acos(cosine))
        
        return angle
    
    def get_landmark_coords(self, landmarks, landmark_id, width, height):
        """
        Get pixel coordinates for a landmark.
        
        Args:
            landmarks: MediaPipe landmarks
            landmark_id: Landmark ID to retrieve
            width, height: Image dimensions
            
        Returns:
            Tuple of (x, y) pixel coordinates
        """
        if landmarks is None:
            return None
        landmark = landmarks.landmark[landmark_id]
        return (int(landmark.x * width), int(landmark.y * height))
    
    def check_pushup_form(self, landmarks, width, height):
        """
        Check push-up form.
        
        Returns:
            Dictionary with form feedback and rep counting
        """
        # Get key landmarks
        left_shoulder = self.get_landmark_coords(landmarks, 
            self.mp_pose.PoseLandmark.LEFT_SHOULDER.value, width, height)
        left_elbow = self.get_landmark_coords(landmarks,
            self.mp_pose.PoseLandmark.LEFT_ELBOW.value, width, height)
        left_wrist = self.get_landmark_coords(landmarks,
            self.mp_pose.PoseLandmark.LEFT_WRIST.value, width, height)
        left_hip = self.get_landmark_coords(landmarks,
            self.mp_pose.PoseLandmark.LEFT_HIP.value, width, height)
        left_knee = self.get_landmark_coords(landmarks,
            self.mp_pose.PoseLandmark.LEFT_KNEE.value, width, height)
        
        if None in [left_shoulder, left_elbow, left_wrist, left_hip, left_knee]:
            return {'feedback': 'Position yourself so camera can see your full body', 'reps': self.rep_count}
        
        # Calculate elbow angle
        elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        
        # Calculate body alignment (hip angle)
        body_angle = self.calculate_angle(left_shoulder, left_hip, left_knee)
        
        # Rep counting logic
        feedback_items = []
        if elbow_angle > 160:
            current_state = 'up'
        elif elbow_angle < 100:
            current_state = 'down'
        else:
            current_state = 'mid'
        
        if self.last_state == 'down' and current_state == 'up':
            self.rep_count += 1
        self.last_state = current_state
        
        # Form checking
        if body_angle < 160 or body_angle > 200:
            feedback_items.append('Keep body straight')
        
        if elbow_angle < 70:
            feedback_items.append('Good depth!')
        elif elbow_angle < 100 and elbow_angle >= 70:
            feedback_items.append('Lower a bit more')
        
        feedback = ' • '.join(feedback_items) if feedback_items else 'Good form!'
        
        return {
            'feedback': feedback,
            'reps': self.rep_count,
            'elbow_angle': elbow_angle,
            'body_angle': body_angle
        }
    
    def check_squat_form(self, landmarks, width, height):
        """
        Check squat form.
        
        Returns:
            Dictionary with form feedback and rep counting
        """
        # Get key landmarks
        left_hip = self.get_landmark_coords(landmarks,
            self.mp_pose.PoseLandmark.LEFT_HIP.value, width, height)
        left_knee = self.get_landmark_coords(landmarks,
            self.mp_pose.PoseLandmark.LEFT_KNEE.value, width, height)
        left_ankle = self.get_landmark_coords(landmarks,
            self.mp_pose.PoseLandmark.LEFT_ANKLE.value, width, height)
        left_shoulder = self.get_landmark_coords(landmarks,
            self.mp_pose.PoseLandmark.LEFT_SHOULDER.value, width, height)
        
        if None in [left_hip, left_knee, left_ankle, left_shoulder]:
            return {'feedback': 'Position yourself in side view', 'reps': self.rep_count}
        
        # Calculate knee angle
        knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        
        # Calculate back angle (torso alignment)
        back_angle = abs(left_shoulder[1] - left_hip[1]) / max(abs(left_shoulder[0] - left_hip[0]), 1)
        
        # Rep counting
        feedback_items = []
        if knee_angle > 160:
            current_state = 'up'
        elif knee_angle < 100:
            current_state = 'down'
        else:
            current_state = 'mid'
        
        if self.last_state == 'down' and current_state == 'up':
            self.rep_count += 1
        self.last_state = current_state
        
        # Form checking
        if knee_angle < 90:
            feedback_items.append('Great depth!')
        elif knee_angle < 110 and knee_angle >= 90:
            feedback_items.append('Good squat')
        elif current_state == 'down':
            feedback_items.append('Go deeper')
        
        if back_angle < 1.5:
            feedback_items.append('Keep chest up')
        
        feedback = ' • '.join(feedback_items) if feedback_items else 'Good form!'
        
        return {
            'feedback': feedback,
            'reps': self.rep_count,
            'knee_angle': knee_angle
        }
    
    def check_plank_form(self, landmarks, width, height):
        """
        Check plank form.
        
        Returns:
            Dictionary with form feedback
        """
        # Get key landmarks
        left_shoulder = self.get_landmark_coords(landmarks,
            self.mp_pose.PoseLandmark.LEFT_SHOULDER.value, width, height)
        left_hip = self.get_landmark_coords(landmarks,
            self.mp_pose.PoseLandmark.LEFT_HIP.value, width, height)
        left_ankle = self.get_landmark_coords(landmarks,
            self.mp_pose.PoseLandmark.LEFT_ANKLE.value, width, height)
        
        if None in [left_shoulder, left_hip, left_ankle]:
            return {'feedback': 'Position in side view', 'reps': 0}
        
        # Check body alignment
        shoulder_y = left_shoulder[1]
        hip_y = left_hip[1]
        ankle_y = left_ankle[1]
        
        feedback_items = []
        
        # Check if hips are sagging
        if hip_y > shoulder_y + 50:
            feedback_items.append('Hips too low - engage core')
        elif hip_y < shoulder_y - 50:
            feedback_items.append('Hips too high - lower them')
        else:
            feedback_items.append('Perfect alignment!')
        
        feedback = ' • '.join(feedback_items) if feedback_items else 'Hold steady!'
        
        return {
            'feedback': feedback,
            'reps': 0
        }
    
    def check_general_form(self, landmarks, width, height):
        """
        General form checking for exercises without specific checks.
        
        Returns:
            Dictionary with basic feedback
        """
        if landmarks is None:
            return {'feedback': 'Position yourself in camera view', 'reps': self.rep_count}
        
        return {
            'feedback': 'Maintain proper form',
            'reps': self.rep_count
        }
    
    def process_frame(self, frame, exercise_id):
        """
        Process frame for exercise-specific form checking.
        
        Args:
            frame: Video frame
            exercise_id: ID of current exercise
            
        Returns:
            Tuple of (processed_frame, feedback_dict)
        """
        # Process frame with pose detection
        processed_frame, tilt_angle, left_shoulder, right_shoulder = \
            self.posture_detector.process_frame(frame)
        
        # Get pose landmarks
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.posture_detector.pose.process(rgb_frame)
        
        feedback = {'feedback': 'No pose detected', 'reps': self.rep_count}
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks
            h, w, c = frame.shape
            
            # Exercise-specific form checking
            if exercise_id == 'pushup':
                feedback = self.check_pushup_form(landmarks, w, h)
            elif exercise_id == 'squat':
                feedback = self.check_squat_form(landmarks, w, h)
            elif exercise_id == 'plank':
                feedback = self.check_plank_form(landmarks, w, h)
            else:
                feedback = self.check_general_form(landmarks, w, h)
        
        # Draw feedback on frame
        cv2.putText(processed_frame, f'Reps: {feedback["reps"]}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Draw feedback text (multiline support)
        feedback_text = feedback['feedback']
        y_offset = 70
        for line in feedback_text.split(' • '):
            cv2.putText(processed_frame, line, (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            y_offset += 30
        
        return processed_frame, feedback
    
    def reset_counter(self):
        """Reset rep counter."""
        self.rep_count = 0
        self.last_state = None
    
    def set_exercise(self, exercise_id):
        """Set current exercise and reset counter."""
        self.current_exercise = exercise_id
        self.reset_counter()
    
    def release(self):
        """Release detector resources."""
        if self.posture_detector:
            self.posture_detector.release()
