#!/usr/bin/env python3
"""
Test script for camera management features.
Tests the database functions and camera detection without running the full UI.
"""

import sys
import os

# Suppress warnings for testing
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['OPENCV_LOG_LEVEL'] = 'ERROR'
os.environ['OPENCV_VIDEOIO_DEBUG'] = '0'

from database import SettingsDatabase
import cv2

# Set OpenCV log level to ERROR only (suppresses WARN messages)
# Only available in OpenCV 4.x
try:
    cv2.setLogLevel(3)
except AttributeError:
    pass  # setLogLevel not available in this OpenCV version


def test_database_camera_functions():
    """Test database camera storage functions."""
    print("Testing database camera functions...")
    
    db_path = 'test_settings.db'
    
    try:
        # Create a test database
        db = SettingsDatabase(db_path)
        
        # Test default camera getter
        default_camera = db.get_default_camera()
        print(f"✓ Default camera (before set): {default_camera}")
        assert default_camera == 0, "Default camera should be 0"
        
        # Test setting camera
        db.set_default_camera(1)
        default_camera = db.get_default_camera()
        print(f"✓ Default camera (after set to 1): {default_camera}")
        assert default_camera == 1, "Default camera should be 1"
        
        # Test setting camera back
        db.set_default_camera(0)
        default_camera = db.get_default_camera()
        print(f"✓ Default camera (after set to 0): {default_camera}")
        assert default_camera == 0, "Default camera should be 0"
        
        print("✓ All database camera tests passed!\n")
        
    finally:
        # Clean up test database
        if os.path.exists(db_path):
            os.remove(db_path)


def test_camera_detection():
    """Test camera detection functionality."""
    print("Testing camera detection...")
    
    cameras_found = []
    
    # Try to detect cameras (up to 5)
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # Try to read a frame
            ret, frame = cap.read()
            
            if ret:
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                cameras_found.append({
                    'index': i,
                    'resolution': f'{int(width)}x{int(height)}',
                    'working': True
                })
                print(f"✓ Camera {i}: {int(width)}x{int(height)} - Working")
            else:
                cameras_found.append({
                    'index': i,
                    'working': False
                })
                print(f"✗ Camera {i}: Opened but failed to read frame")
            
            cap.release()
    
    if cameras_found:
        print(f"\n✓ Found {len(cameras_found)} camera(s)")
    else:
        print("\n! No cameras detected (this is okay if running headless)")
    
    print()


def test_warning_suppression():
    """Test that warnings are properly suppressed."""
    print("Testing warning suppression...")
    
    # Import modules that might produce warnings
    try:
        import warnings
        warnings.filterwarnings('ignore', category=UserWarning, module='google.protobuf')
        warnings.filterwarnings('ignore', category=FutureWarning, module='mediapipe')
        print("✓ Warning filters set up correctly")
    except Exception as e:
        print(f"✗ Error setting up warning filters: {e}")
        return False
    
    # Check environment variables
    if os.environ.get('TF_CPP_MIN_LOG_LEVEL') == '3':
        print("✓ TensorFlow logging suppression enabled")
    else:
        print("✗ TensorFlow logging suppression not set")
    
    print()
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Camera Management Features Test")
    print("=" * 60)
    print()
    
    try:
        # Test 1: Database functions
        test_database_camera_functions()
        
        # Test 2: Camera detection
        test_camera_detection()
        
        # Test 3: Warning suppression
        test_warning_suppression()
        
        print("=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
        return 0
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
