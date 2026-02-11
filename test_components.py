#!/usr/bin/env python3
"""
Test script for posture tracker components.
Tests database and posture detector logic without GUI.
"""

import sys
import os

def test_database():
    """Test database module."""
    print("Testing database module...")
    try:
        from database import SettingsDatabase
        
        # Create test database
        db = SettingsDatabase('test_settings.db')
        
        # Test setting and getting threshold
        db.set_tilt_threshold(20.0)
        threshold = db.get_tilt_threshold()
        assert threshold == 20.0, f"Expected 20.0, got {threshold}"
        
        # Test default value
        default_val = db.get_setting('nonexistent', 'default')
        assert default_val == 'default', f"Expected 'default', got {default_val}"
        
        # Clean up
        if os.path.exists('test_settings.db'):
            os.remove('test_settings.db')
        
        print("✓ Database tests passed")
        return True
    except Exception as e:
        print(f"✗ Database tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_posture_detector_logic():
    """Test posture detector logic (without MediaPipe)."""
    print("\nTesting posture detector logic...")
    try:
        import math
        
        # Test angle calculation logic
        def calculate_tilt(left_shoulder, right_shoulder):
            """Calculate shoulder tilt angle."""
            if left_shoulder is None or right_shoulder is None:
                return 0
            
            x_diff = right_shoulder[0] - left_shoulder[0]
            y_diff = right_shoulder[1] - left_shoulder[1]
            
            angle = math.degrees(math.atan2(y_diff, x_diff))
            return abs(angle)
        
        # Test cases
        # Level shoulders (no tilt)
        left = (100, 100)
        right = (200, 100)
        angle = calculate_tilt(left, right)
        assert angle < 1.0, f"Level shoulders should have ~0 tilt, got {angle}"
        
        # Tilted shoulders
        left = (100, 100)
        right = (200, 120)  # Right shoulder lower
        angle = calculate_tilt(left, right)
        assert 10 < angle < 15, f"Tilted shoulders should have ~11 degrees, got {angle}"
        
        # None handling
        angle = calculate_tilt(None, right)
        assert angle == 0, f"None should return 0, got {angle}"
        
        print("✓ Posture detector logic tests passed")
        return True
    except Exception as e:
        print(f"✗ Posture detector logic tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_imports():
    """Test that all required modules can be imported."""
    print("\nTesting module imports...")
    modules_ok = True
    
    # Test standard library imports
    try:
        import sqlite3
        print("✓ sqlite3 imported")
    except ImportError as e:
        print(f"✗ Failed to import sqlite3: {e}")
        modules_ok = False
    
    try:
        import math
        print("✓ math imported")
    except ImportError as e:
        print(f"✗ Failed to import math: {e}")
        modules_ok = False
    
    # Test our modules
    try:
        from database import SettingsDatabase
        print("✓ database module imported")
    except ImportError as e:
        print(f"✗ Failed to import database: {e}")
        modules_ok = False
    
    return modules_ok

def main():
    """Run all tests."""
    print("=" * 60)
    print("Posture Tracker - Component Tests")
    print("=" * 60)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test database
    if not test_database():
        all_passed = False
    
    # Test posture detector logic
    if not test_posture_detector_logic():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("All tests PASSED ✓")
        return 0
    else:
        print("Some tests FAILED ✗")
        return 1

if __name__ == '__main__':
    sys.exit(main())
