#!/usr/bin/env python3
"""
Test to verify the widget availability timing fix.
This test verifies the changes in the main.py file without running Kivy.
"""

import sys
import os

def test_initial_delay_increased():
    """Test that initial delays have been increased."""
    print("Testing initial delay increases...")
    
    # Read the main.py file to verify delay values
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Check camera spinner delay increased to 0.5
    if "Clock.schedule_once(self.populate_camera_list, 0.5)" in content:
        print("  ✓ Camera spinner initial delay is 0.5s")
    else:
        print("  ✗ Camera spinner initial delay should be 0.5s")
        return False
    
    # Check settings load delay increased to 0.5
    if "Clock.schedule_once(lambda dt: self.root.load_settings(), 0.5)" in content:
        print("  ✓ Settings load initial delay is 0.5s")
    else:
        print("  ✗ Settings load initial delay should be 0.5s")
        return False
    
    return True

def test_log_level_changed():
    """Test that log level changed from WARNING to DEBUG for retries."""
    print("\nTesting log level changes...")
    
    # Read the main.py file
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Verify Logger.warning is no longer used for retries
    if "Logger.warning(f\"threshold_input not yet available" in content:
        print("  ✗ Logger.warning should not be used for threshold_input retries")
        return False
    else:
        print("  ✓ Logger.warning not used for threshold_input retries")
    
    # Verify Logger.debug is used instead
    if "Logger.debug(f\"threshold_input not yet available" in content:
        print("  ✓ Logger.debug used for threshold_input retries")
    else:
        print("  ✗ Logger.debug should be used for threshold_input retries")
        return False
    
    if "Logger.debug(f\"camera_spinner not yet available" in content:
        print("  ✓ Logger.debug used for camera_spinner retries")
    else:
        print("  ✗ Logger.debug should be used for camera_spinner retries")
        return False
    
    return True

def test_logging_intervals():
    """Test that logging only happens at specific intervals."""
    print("\nTesting logging interval logic...")
    
    # Read the main.py file
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Check for interval logging in camera_spinner
    if "if self._camera_list_retry_count == 1 or self._camera_list_retry_count % 10 == 0:" in content:
        print("  ✓ Camera spinner uses interval logging (1st, 10th, 20th, etc.)")
    else:
        print("  ✗ Camera spinner should use interval logging")
        return False
    
    # Check for interval logging in threshold_input
    if "if self._settings_load_retry_count == 1 or self._settings_load_retry_count % 10 == 0:" in content:
        print("  ✓ Threshold input uses interval logging (1st, 10th, 20th, etc.)")
    else:
        print("  ✗ Threshold input should use interval logging")
        return False
    
    return True

def test_error_logging_preserved():
    """Test that error logging is still present for max retries."""
    print("\nTesting error logging preservation...")
    
    # Read the main.py file
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Check camera spinner error
    if 'Logger.error("Camera spinner not available after 5 seconds")' in content:
        print("  ✓ Camera spinner error logging preserved")
    else:
        print("  ✗ Camera spinner error logging should be preserved")
        return False
    
    # Check threshold input error
    if 'Logger.error("threshold_input not available after maximum retries")' in content:
        print("  ✓ Threshold input error logging preserved")
    else:
        print("  ✗ Threshold input error logging should be preserved")
        return False
    
    return True

def main():
    """Run all timing fix tests."""
    print("=" * 60)
    print("Widget Availability Timing Fix - Verification")
    print("=" * 60)
    print()
    
    all_passed = True
    
    if not test_initial_delay_increased():
        all_passed = False
    
    if not test_log_level_changed():
        all_passed = False
    
    if not test_logging_intervals():
        all_passed = False
    
    if not test_error_logging_preserved():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("All verification checks PASSED ✓")
        print()
        print("Summary of fixes:")
        print("  • Initial delays increased from 0.1s/0.2s to 0.5s")
        print("  • Retry logging changed from WARNING to DEBUG level")
        print("  • Logging reduced to intervals (1st, 10th, 20th, etc.)")
        print("  • Final error logging preserved for diagnostics")
        return 0
    else:
        print("Some verification checks FAILED ✗")
        return 1

if __name__ == '__main__':
    sys.exit(main())

