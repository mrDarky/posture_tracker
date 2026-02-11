#!/usr/bin/env python
"""
Test script to verify that the Posture Tracker app can start successfully.
This script tests that the app initializes without crashing.
"""

import sys
import os
import threading
import time

# Set up environment for headless testing
os.environ['KIVY_NO_CONSOLELOG'] = '0'
os.environ['KIVY_NO_ARGS'] = '1'  # Disable Kivy argument parsing

print("=" * 60)
print("Testing Posture Tracker App Startup")
print("=" * 60)

try:
    # Import the main module
    print("\n1. Importing main module...")
    import main
    print("   ✓ Module imported successfully")
    
    # Verify classes exist
    print("\n2. Verifying classes...")
    assert hasattr(main, 'MainApp'), "MainApp class not found"
    assert hasattr(main, 'PostureTrackerApp'), "PostureTrackerApp class not found"
    print("   ✓ All required classes present")
    
    # Test database initialization
    print("\n3. Testing database initialization...")
    from database import SettingsDatabase
    # Use a temporary file database for testing
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as f:
        temp_db_path = f.name
    try:
        test_db = SettingsDatabase(temp_db_path)
        assert test_db.get_tilt_threshold() == 15.0, "Default threshold incorrect"
        print("   ✓ Database initializes correctly")
    finally:
        # Clean up temp database
        if os.path.exists(temp_db_path):
            os.unlink(temp_db_path)
    
    # Test detector initialization
    print("\n4. Testing PostureDetector initialization...")
    from posture_detector import PostureDetector
    test_detector = PostureDetector()
    test_detector.release()
    print("   ✓ PostureDetector initializes correctly")
    
    # Test app instantiation (without building UI, which requires main thread)
    print("\n5. Testing app instantiation...")
    try:
        app = main.MainApp()
        print("   ✓ App instantiated without crashing")
    except Exception as e:
        raise Exception(f"Failed to instantiate app: {e}")
    
    print("\n" + "=" * 60)
    print("SUCCESS: All startup tests passed!")
    print("=" * 60)
    print("\nNote: The app can now be started with 'python main.py'")
    print("It should display a window and not crash immediately.")
    sys.exit(0)
    
except Exception as e:
    print(f"\n{'=' * 60}")
    print(f"FAILED: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
    sys.exit(1)
