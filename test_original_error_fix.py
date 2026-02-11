#!/usr/bin/env python3
"""
Test to reproduce and verify the fix for the original AttributeError:
'PostureTrackerApp' object has no attribute 'is_tracking'

This test specifically validates that the error mentioned in line 176 of main.py
in the update_ui_colors method no longer occurs.
"""

import sys
import os

# Set up headless mode
os.environ['KIVY_NO_CONSOLELOG'] = '0'
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_GL_BACKEND'] = 'mock'

print("=" * 60)
print("Testing Original AttributeError Fix")
print("=" * 60)
print("\nOriginal error:")
print('  posture_tracker/main.py", line 176, in update_ui_colors')
print('     if \'status_label\' in self.ids and not self.is_tracking:')
print('                                           ^^^^^^^^^^^^^^^^')
print('  AttributeError: \'PostureTrackerApp\' object has no attribute \'is_tracking\'')
print()

try:
    from kivy.config import Config
    Config.set('graphics', 'width', '100')
    Config.set('graphics', 'height', '100')
    
    import unittest.mock as mock
    
    # Simulate the exact scenario where the error occurred
    print("1. Simulating app initialization (where error occurred)...")
    
    with mock.patch('kivy.core.window.Window'), \
         mock.patch('main.PostureDetector') as mock_detector, \
         mock.patch('main.SettingsDatabase') as mock_db:
        
        # Set up mocks
        mock_db_instance = mock.MagicMock()
        mock_db_instance.get_theme.return_value = 'dark'
        mock_db.return_value = mock_db_instance
        
        # Import after setting up mocks
        import main
        
        # This is where the error occurred - during __init__, apply_theme is called
        # which then calls update_ui_colors, which tried to access self.is_tracking
        print("   Creating PostureTrackerApp (triggers apply_theme -> update_ui_colors)...")
        
        try:
            app = main.PostureTrackerApp()
            print("   ✓ App created successfully without AttributeError!")
        except AttributeError as e:
            if 'is_tracking' in str(e):
                print(f"   ✗ FAILED: Original AttributeError still occurs: {e}")
                sys.exit(1)
            else:
                raise
    
    print("\n2. Verifying is_tracking is accessible in update_ui_colors...")
    
    with mock.patch('kivy.core.window.Window'), \
         mock.patch('main.PostureDetector'), \
         mock.patch('main.SettingsDatabase') as mock_db:
        
        mock_db_instance = mock.MagicMock()
        mock_db_instance.get_theme.return_value = 'light'
        mock_db.return_value = mock_db_instance
        
        app = main.PostureTrackerApp()
        
        # Call update_ui_colors directly (line 168 onwards in main.py)
        # This includes the problematic line 176
        try:
            app.update_ui_colors()
            print("   ✓ update_ui_colors() executed without error")
        except AttributeError as e:
            if 'is_tracking' in str(e):
                print(f"   ✗ FAILED: AttributeError in update_ui_colors: {e}")
                sys.exit(1)
            else:
                raise
        
        # Verify the attribute exists and has correct value
        assert hasattr(app, 'is_tracking'), "is_tracking attribute not found"
        assert app.is_tracking is False, f"is_tracking should be False, got {app.is_tracking}"
        print("   ✓ is_tracking attribute exists and has correct value (False)")
    
    print("\n3. Testing with tracking state changes...")
    
    with mock.patch('kivy.core.window.Window'), \
         mock.patch('main.PostureDetector'), \
         mock.patch('main.SettingsDatabase') as mock_db:
        
        mock_db_instance = mock.MagicMock()
        mock_db_instance.get_theme.return_value = 'dark'
        mock_db.return_value = mock_db_instance
        
        app = main.PostureTrackerApp()
        
        # Verify we can change is_tracking state
        app.is_tracking = True
        app.update_ui_colors()
        print("   ✓ update_ui_colors() works with is_tracking=True")
        
        app.is_tracking = False
        app.update_ui_colors()
        print("   ✓ update_ui_colors() works with is_tracking=False")
    
    print("\n" + "=" * 60)
    print("SUCCESS: Original AttributeError is FIXED!")
    print("=" * 60)
    print("\nThe issue at line 176 in update_ui_colors is resolved:")
    print("  - is_tracking is now initialized before apply_theme() is called")
    print("  - update_ui_colors can safely access self.is_tracking")
    print("  - No AttributeError occurs during app initialization")
    sys.exit(0)
    
except Exception as e:
    print(f"\n{'=' * 60}")
    print(f"FAILED: Unexpected error: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
    sys.exit(1)
