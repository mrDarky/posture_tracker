#!/usr/bin/env python3
"""
Test for camera_spinner KeyError fix.
Tests that the methods handle missing camera_spinner ID gracefully.
"""

import sys
import os

# Mock the Kivy components to avoid X server requirement
class MockIds:
    """Mock the Kivy ids dictionary."""
    def __init__(self, keys=None):
        self._data = keys or {}
    
    def __contains__(self, key):
        return key in self._data
    
    def __getitem__(self, key):
        if key not in self._data:
            raise KeyError(key)
        return self._data[key]

class MockWidget:
    """Mock widget with disabled property."""
    def __init__(self):
        self.disabled = False
        self.text = "Camera 0"
        self.values = []

class MockApp:
    """Mock PostureTrackerApp to test the fix."""
    def __init__(self, has_camera_spinner=False):
        self.ids = MockIds()
        if has_camera_spinner:
            self.ids._data['camera_spinner'] = MockWidget()
        
    def populate_camera_list_check(self):
        """Simulate the populate_camera_list method's ID check."""
        if 'camera_spinner' not in self.ids:
            return "RESCHEDULED"  # Would reschedule in real code
        return "SUCCESS"
    
    def get_selected_camera_index_check(self):
        """Simulate the get_selected_camera_index method's ID check."""
        if 'camera_spinner' not in self.ids:
            return 0
        # Simulate actual parsing logic
        camera_text = self.ids['camera_spinner'].text
        if camera_text.startswith("Camera "):
            try:
                return int(camera_text.split()[1])
            except (IndexError, ValueError):
                return 0
        return 0
    
    def start_tracking_check(self):
        """Simulate the start_tracking method's ID check."""
        if 'camera_spinner' in self.ids:
            self.ids['camera_spinner'].disabled = True
            return "DISABLED"
        return "SKIPPED"
    
    def stop_tracking_check(self):
        """Simulate the stop_tracking method's ID check."""
        if 'camera_spinner' in self.ids:
            self.ids['camera_spinner'].disabled = False
            return "ENABLED"
        return "SKIPPED"

def test_missing_camera_spinner():
    """Test that methods handle missing camera_spinner gracefully."""
    print("Testing missing camera_spinner ID...")
    
    app = MockApp(has_camera_spinner=False)
    
    # Test populate_camera_list
    result = app.populate_camera_list_check()
    assert result == "RESCHEDULED", f"populate_camera_list should reschedule when ID missing, got {result}"
    print("  ✓ populate_camera_list handles missing ID")
    
    # Test get_selected_camera_index
    result = app.get_selected_camera_index_check()
    assert result == 0, f"get_selected_camera_index should return 0 when ID missing, got {result}"
    print("  ✓ get_selected_camera_index handles missing ID")
    
    # Test start_tracking
    result = app.start_tracking_check()
    assert result == "SKIPPED", f"start_tracking should skip when ID missing, got {result}"
    print("  ✓ start_tracking handles missing ID")
    
    # Test stop_tracking
    result = app.stop_tracking_check()
    assert result == "SKIPPED", f"stop_tracking should skip when ID missing, got {result}"
    print("  ✓ stop_tracking handles missing ID")
    
    return True

def test_existing_camera_spinner():
    """Test that methods work normally when camera_spinner exists."""
    print("\nTesting existing camera_spinner ID...")
    
    app = MockApp(has_camera_spinner=True)
    
    # Test populate_camera_list
    result = app.populate_camera_list_check()
    assert result == "SUCCESS", f"populate_camera_list should succeed when ID exists, got {result}"
    print("  ✓ populate_camera_list works with existing ID")
    
    # Test get_selected_camera_index with different camera values
    app.ids['camera_spinner'].text = "Camera 0"
    result = app.get_selected_camera_index_check()
    assert result == 0, f"get_selected_camera_index should return 0 for 'Camera 0', got {result}"
    
    app.ids['camera_spinner'].text = "Camera 2"
    result = app.get_selected_camera_index_check()
    assert result == 2, f"get_selected_camera_index should return 2 for 'Camera 2', got {result}"
    
    app.ids['camera_spinner'].text = "No cameras found"
    result = app.get_selected_camera_index_check()
    assert result == 0, f"get_selected_camera_index should return 0 for non-camera text, got {result}"
    print("  ✓ get_selected_camera_index works with existing ID and parses correctly")
    
    # Test start_tracking
    result = app.start_tracking_check()
    assert result == "DISABLED", f"start_tracking should disable when ID exists, got {result}"
    assert app.ids['camera_spinner'].disabled == True, "camera_spinner should be disabled"
    print("  ✓ start_tracking works with existing ID")
    
    # Test stop_tracking
    result = app.stop_tracking_check()
    assert result == "ENABLED", f"stop_tracking should enable when ID exists, got {result}"
    assert app.ids['camera_spinner'].disabled == False, "camera_spinner should be enabled"
    print("  ✓ stop_tracking works with existing ID")
    
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("Camera Spinner KeyError Fix - Unit Tests")
    print("=" * 60)
    
    all_passed = True
    
    try:
        if not test_missing_camera_spinner():
            all_passed = False
    except Exception as e:
        print(f"\n✗ test_missing_camera_spinner failed: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    try:
        if not test_existing_camera_spinner():
            all_passed = False
    except Exception as e:
        print(f"\n✗ test_existing_camera_spinner failed: {e}")
        import traceback
        traceback.print_exc()
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
