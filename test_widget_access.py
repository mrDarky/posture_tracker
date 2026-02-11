#!/usr/bin/env python3
"""
Test to verify that threshold_input widget access is safe.
This tests the fix for KeyError when accessing threshold_input.
"""

import sys
import os
import tempfile
from unittest.mock import Mock, MagicMock
from kivy.logger import Logger

def test_save_settings_without_widgets():
    """Test that save_settings handles missing widgets gracefully."""
    print("Testing save_settings() with missing widgets...")
    
    # Mock the required imports
    sys.path.insert(0, os.path.dirname(__file__))
    from main import PostureTrackerApp
    
    # Create app instance
    app = PostureTrackerApp()
    
    # Mock the ids dictionary to simulate missing widgets
    app.ids = {}
    
    # This should not raise KeyError
    try:
        app.save_settings()
        print("✓ save_settings() handled missing widgets gracefully")
        return True
    except KeyError as e:
        print(f"✗ save_settings() raised KeyError: {e}")
        return False
    except Exception as e:
        print(f"✗ save_settings() raised unexpected error: {e}")
        return False

def test_load_settings_without_widgets():
    """Test that load_settings handles missing widgets gracefully."""
    print("\nTesting load_settings() with missing widgets...")
    
    from main import PostureTrackerApp
    
    # Create app instance
    app = PostureTrackerApp()
    
    # Mock the ids dictionary to simulate missing widgets
    app.ids = {}
    
    # This should not raise KeyError
    try:
        app.load_settings()
        print("✓ load_settings() handled missing widgets gracefully")
        return True
    except KeyError as e:
        print(f"✗ load_settings() raised KeyError: {e}")
        return False
    except Exception as e:
        print(f"✗ load_settings() raised unexpected error: {e}")
        return False

def test_save_settings_with_widgets():
    """Test that save_settings works correctly when widgets are present."""
    print("\nTesting save_settings() with available widgets...")
    
    from main import PostureTrackerApp
    
    # Create app instance
    app = PostureTrackerApp()
    
    # Mock the ids dictionary with required widgets
    mock_input = Mock()
    mock_input.text = "20.0"
    
    mock_status = Mock()
    mock_status.text = ""
    mock_status.color = (0, 0, 0, 1)
    
    app.ids = {
        'threshold_input': mock_input,
        'settings_status': mock_status
    }
    
    # This should work correctly
    try:
        app.save_settings()
        # Check that the status was updated
        assert "Settings saved!" in mock_status.text
        print("✓ save_settings() worked correctly with widgets present")
        return True
    except Exception as e:
        print(f"✗ save_settings() failed with widgets present: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_load_settings_with_widgets():
    """Test that load_settings works correctly when widgets are present."""
    print("\nTesting load_settings() with available widgets...")
    
    from main import PostureTrackerApp
    from database import DEFAULT_TILT_THRESHOLD
    
    # Create app instance
    app = PostureTrackerApp()
    
    # Mock the ids dictionary with required widget
    mock_input = Mock()
    mock_input.text = ""
    
    app.ids = {
        'threshold_input': mock_input
    }
    
    # This should work correctly
    try:
        app.load_settings()
        # Check that the input was populated with the default threshold
        expected = str(DEFAULT_TILT_THRESHOLD)
        assert mock_input.text == expected, f"Expected '{expected}', got '{mock_input.text}'"
        print("✓ load_settings() worked correctly with widgets present")
        return True
    except Exception as e:
        print(f"✗ load_settings() failed with widgets present: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all widget access tests."""
    print("=" * 60)
    print("Widget Access Safety Tests")
    print("=" * 60)
    
    all_passed = True
    
    # Test missing widgets (the fix)
    if not test_save_settings_without_widgets():
        all_passed = False
    
    if not test_load_settings_without_widgets():
        all_passed = False
    
    # Test with widgets present (functionality preserved)
    if not test_save_settings_with_widgets():
        all_passed = False
    
    if not test_load_settings_with_widgets():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("All widget access tests PASSED ✓")
        return 0
    else:
        print("Some widget access tests FAILED ✗")
        return 1

if __name__ == '__main__':
    sys.exit(main())
