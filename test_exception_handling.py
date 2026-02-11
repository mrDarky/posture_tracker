#!/usr/bin/env python
"""
Test script to verify exception handling in database operations.
This ensures that database errors don't cause silent crashes.
"""

import sys
import os
import tempfile
import sqlite3

# Set up environment for headless testing
os.environ['KIVY_NO_CONSOLELOG'] = '0'
os.environ['KIVY_NO_ARGS'] = '1'

print("=" * 60)
print("Testing Exception Handling for Database Operations")
print("=" * 60)

try:
    # Import the database module
    print("\n1. Testing database with permissions error...")
    from database import SettingsDatabase
    
    # Create a temporary database file
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.db') as f:
        temp_db_path = f.name
    
    # Initialize database normally
    db = SettingsDatabase(temp_db_path)
    db.set_tilt_threshold(20.0)
    print("   ✓ Database initialized normally")
    
    # Make the database file read-only to simulate permission errors
    os.chmod(temp_db_path, 0o444)
    
    # Test that write operations raise exceptions
    try:
        db.set_tilt_threshold(25.0)
        print("   ✗ Should have raised exception on read-only database")
        sys.exit(1)
    except Exception as e:
        print(f"   ✓ Write to read-only database raises exception: {type(e).__name__}")
    
    # Clean up
    os.chmod(temp_db_path, 0o644)
    os.unlink(temp_db_path)
    
    # Test with corrupted database
    print("\n2. Testing database with corruption...")
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.db') as f:
        temp_db_path = f.name
        # Write invalid data to create a corrupted database
        f.write(b'This is not a valid SQLite database file!')
    
    try:
        db = SettingsDatabase(temp_db_path)
        print("   ✗ Should have raised exception on corrupted database")
        os.unlink(temp_db_path)
        sys.exit(1)
    except Exception as e:
        print(f"   ✓ Corrupted database raises exception: {type(e).__name__}")
        os.unlink(temp_db_path)
    
    # Test with non-existent directory
    print("\n3. Testing database with invalid path...")
    try:
        db = SettingsDatabase('/nonexistent_dir/subdir/test.db')
        print("   ✗ Should have raised exception with invalid path")
        sys.exit(1)
    except Exception as e:
        print(f"   ✓ Invalid path raises exception: {type(e).__name__}")
    
    # Test main app with database errors
    print("\n4. Testing main app with mock database errors...")
    import main
    from unittest.mock import Mock, MagicMock
    from kivy.clock import Clock
    
    # Create app instance
    app = main.PostureTrackerApp()
    
    # Mock the database to raise exceptions
    app.db = Mock()
    app.db.set_tilt_threshold = Mock(side_effect=sqlite3.OperationalError("Simulated database error"))
    app.db.get_tilt_threshold = Mock(side_effect=sqlite3.OperationalError("Simulated database error"))
    app.db.set_default_camera = Mock(side_effect=sqlite3.OperationalError("Simulated database error"))
    app.db.set_theme = Mock(side_effect=sqlite3.OperationalError("Simulated database error"))
    
    # Mock the UI widgets
    app.ids = {
        'threshold_input': Mock(text='20.0'),
        'settings_status': Mock(text='', color=(1, 1, 1, 1)),
        'camera_scan_status': Mock(text='', color=(1, 1, 1, 1)),
    }
    
    # Test save_settings with database error
    print("\n   Testing save_settings() with database error...")
    try:
        app.save_settings()
        print("   ✓ save_settings() handles database error gracefully")
    except Exception as e:
        print(f"   ✗ save_settings() raised unhandled exception: {e}")
        sys.exit(1)
    
    # Test set_default_camera with database error
    print("   Testing set_default_camera() with database error...")
    try:
        app.set_default_camera(0)
        print("   ✓ set_default_camera() handles database error gracefully")
    except Exception as e:
        print(f"   ✗ set_default_camera() raised unhandled exception: {e}")
        sys.exit(1)
    
    # Test change_theme with database error
    print("   Testing change_theme() with database error...")
    try:
        app.change_theme('light')
        print("   ✓ change_theme() handles database error gracefully")
    except Exception as e:
        print(f"   ✗ change_theme() raised unhandled exception: {e}")
        sys.exit(1)
    
    # Test load_settings with database error
    print("   Testing load_settings() with database error...")
    try:
        app.load_settings()
        print("   ✓ load_settings() handles database error gracefully")
    except Exception as e:
        print(f"   ✗ load_settings() raised unhandled exception: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("SUCCESS: All exception handling tests passed!")
    print("=" * 60)
    print("\nDatabase errors are now handled gracefully and won't cause")
    print("silent crashes on startup or during runtime.")
    sys.exit(0)
    
except Exception as e:
    print(f"\n{'=' * 60}")
    print(f"FAILED: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
    sys.exit(1)
