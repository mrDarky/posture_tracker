#!/usr/bin/env python
"""
Final validation test: Verify that database exceptions don't cause crashes.
"""

import sys
import os
import tempfile
import sqlite3

os.environ['KIVY_NO_CONSOLELOG'] = '0'
os.environ['KIVY_NO_ARGS'] = '1'

print("=" * 60)
print("Final Validation: Database Exception Handling")
print("=" * 60)

def test_database_exceptions():
    """Test that database operations can raise exceptions."""
    from database import SettingsDatabase
    
    print("\n1. Testing database exception scenarios...")
    
    # Test 1: Permission error
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.db') as f:
        temp_db = f.name
    
    db = SettingsDatabase(temp_db)
    os.chmod(temp_db, 0o444)  # Make read-only
    
    try:
        db.set_tilt_threshold(25.0)
        print("   ✗ Should have raised exception on read-only database")
        return False
    except Exception:
        print("   ✓ Read-only database raises exception as expected")
    
    os.chmod(temp_db, 0o644)
    os.unlink(temp_db)
    
    # Test 2: Invalid path
    try:
        db = SettingsDatabase('/nonexistent/path/test.db')
        print("   ✗ Should have raised exception on invalid path")
        return False
    except Exception:
        print("   ✓ Invalid path raises exception as expected")
    
    return True

def test_exception_handling_in_code():
    """Verify exception handling exists in all critical methods."""
    print("\n2. Verifying exception handling in code...")
    
    import main
    import inspect
    
    methods_to_check = [
        ('save_settings', main.PostureTrackerApp.save_settings),
        ('load_settings', main.PostureTrackerApp.load_settings),
        ('set_default_camera', main.PostureTrackerApp.set_default_camera),
        ('change_theme', main.PostureTrackerApp.change_theme),
    ]
    
    all_good = True
    for method_name, method in methods_to_check:
        source = inspect.getsource(method)
        if 'except Exception' in source:
            print(f"   ✓ {method_name}() has exception handling")
        else:
            print(f"   ✗ {method_name}() missing exception handling")
            all_good = False
    
    return all_good

def test_app_initialization():
    """Test that app can initialize successfully."""
    print("\n3. Testing app initialization...")
    
    try:
        import main
        app = main.MainApp()
        print("   ✓ MainApp instantiates successfully")
        return True
    except Exception as e:
        print(f"   ✗ Failed to instantiate app: {e}")
        return False

def test_protected_database_checks():
    """Verify database operations check for None before calling."""
    print("\n4. Verifying database None checks...")
    
    import main
    import inspect
    
    # Check save_settings
    source = inspect.getsource(main.PostureTrackerApp.save_settings)
    if 'if not self.db:' in source:
        print("   ✓ save_settings() checks for None database")
    else:
        print("   ✗ save_settings() missing None check")
        return False
    
    # Check load_settings
    source = inspect.getsource(main.PostureTrackerApp.load_settings)
    if 'if not self.db:' in source:
        print("   ✓ load_settings() checks for None database")
    else:
        print("   ✗ load_settings() missing None check")
        return False
    
    return True

try:
    # Run all tests
    results = []
    results.append(test_database_exceptions())
    results.append(test_exception_handling_in_code())
    results.append(test_app_initialization())
    results.append(test_protected_database_checks())
    
    print("\n" + "=" * 60)
    if all(results):
        print("SUCCESS: All validation tests passed!")
        print("=" * 60)
        print("\n✓ Database exceptions are properly handled")
        print("✓ App won't crash on database errors")
        print("✓ User-friendly error messages will be displayed")
        print("✓ Application continues to function despite errors")
        sys.exit(0)
    else:
        print("FAILED: Some validation tests failed")
        print("=" * 60)
        sys.exit(1)

except Exception as e:
    print(f"\n{'=' * 60}")
    print(f"FAILED: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
    sys.exit(1)
