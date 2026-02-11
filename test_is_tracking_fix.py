#!/usr/bin/env python3
"""
Test script to verify that the is_tracking AttributeError is fixed.
This test checks that is_tracking is properly initialized before apply_theme is called.
"""

import sys
import os

# Set up headless mode
os.environ['KIVY_NO_CONSOLELOG'] = '0'
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_GL_BACKEND'] = 'mock'

print("=" * 60)
print("Testing is_tracking initialization fix")
print("=" * 60)

try:
    print("\n1. Testing initialization order...")
    
    # Import required modules
    from kivy.config import Config
    Config.set('graphics', 'width', '100')
    Config.set('graphics', 'height', '100')
    
    # Mock the display
    import unittest.mock as mock
    with mock.patch('kivy.core.window.Window'):
        # Import main module (this will execute class definitions)
        import main
        
        # Verify that PostureTrackerApp has the is_tracking attribute
        # Create mock for detector and database
        with mock.patch('main.PostureDetector'), \
             mock.patch('main.SettingsDatabase') as mock_db:
            
            # Set up mock database to return 'dark' theme
            mock_db_instance = mock.MagicMock()
            mock_db_instance.get_theme.return_value = 'dark'
            mock_db.return_value = mock_db_instance
            
            # This should not raise AttributeError
            print("   Creating PostureTrackerApp instance...")
            app = main.PostureTrackerApp()
            
            # Verify is_tracking exists and is False
            assert hasattr(app, 'is_tracking'), "is_tracking attribute missing"
            assert app.is_tracking is False, "is_tracking should be False initially"
            
            print("   ✓ is_tracking properly initialized before apply_theme")
    
    print("\n2. Testing that update_ui_colors can access is_tracking...")
    
    # Create another instance and call update_ui_colors directly
    with mock.patch('kivy.core.window.Window'), \
         mock.patch('main.PostureDetector'), \
         mock.patch('main.SettingsDatabase') as mock_db:
        
        mock_db_instance = mock.MagicMock()
        mock_db_instance.get_theme.return_value = 'dark'
        mock_db.return_value = mock_db_instance
        
        app = main.PostureTrackerApp()
        
        # This should not raise AttributeError
        app.update_ui_colors()
        print("   ✓ update_ui_colors can access is_tracking without error")
    
    print("\n" + "=" * 60)
    print("SUCCESS: is_tracking initialization fix verified!")
    print("=" * 60)
    sys.exit(0)
    
except AttributeError as e:
    if 'is_tracking' in str(e):
        print(f"\n{'=' * 60}")
        print(f"FAILED: AttributeError still exists: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    else:
        raise

except Exception as e:
    print(f"\n{'=' * 60}")
    print(f"FAILED: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
    sys.exit(1)
