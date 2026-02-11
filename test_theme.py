#!/usr/bin/env python3
"""
Test script for theme functionality.
Tests theme switching and database storage.
"""

import sys
import os


def test_theme_database():
    """Test theme storage in database."""
    print("Testing theme database storage...")
    try:
        from database import SettingsDatabase
        
        # Create test database
        db = SettingsDatabase('test_theme_settings.db')
        
        # Test default theme
        default_theme = db.get_theme()
        assert default_theme == 'dark', f"Expected 'dark', got {default_theme}"
        
        # Test setting light theme
        db.set_theme('light')
        theme = db.get_theme()
        assert theme == 'light', f"Expected 'light', got {theme}"
        
        # Test setting dark theme
        db.set_theme('dark')
        theme = db.get_theme()
        assert theme == 'dark', f"Expected 'dark', got {theme}"
        
        # Test invalid theme
        try:
            db.set_theme('invalid')
            assert False, "Should have raised ValueError for invalid theme"
        except ValueError as e:
            assert "Theme must be 'dark' or 'light'" in str(e)
        
        # Clean up
        if os.path.exists('test_theme_settings.db'):
            os.remove('test_theme_settings.db')
        
        print("✓ Theme database tests passed")
        return True
    except Exception as e:
        print(f"✗ Theme database tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_theme_colors():
    """Test that both theme color palettes are defined correctly."""
    print("\nTesting theme color palettes...")
    try:
        # Read and parse theme definitions from main.py
        # Note: Using exec() here is safe as we're only reading from our own codebase
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Extract DARK_THEME dictionary
        dark_start = content.find('DARK_THEME = {')
        dark_end = content.find('}', dark_start) + 1
        dark_theme_str = content[dark_start:dark_end]
        
        # Extract LIGHT_THEME dictionary
        light_start = content.find('LIGHT_THEME = {')
        light_end = content.find('}', light_start) + 1
        light_theme_str = content[light_start:light_end]
        
        # Execute to get the dictionaries
        # Safe in test context - only evaluating our own theme definitions
        exec_globals = {}
        exec(dark_theme_str, exec_globals)
        exec(light_theme_str, exec_globals)
        
        DARK_THEME = exec_globals['DARK_THEME']
        LIGHT_THEME = exec_globals['LIGHT_THEME']
        
        # Check that all required color keys exist in both themes
        required_keys = [
            'background', 'surface', 'surface_variant', 'text', 'text_muted',
            'text_dimmed', 'neutral', 'good', 'bad', 'accent', 'scanning',
            'tab_bg', 'tab_text'
        ]
        
        for key in required_keys:
            assert key in DARK_THEME, f"Missing '{key}' in DARK_THEME"
            assert key in LIGHT_THEME, f"Missing '{key}' in LIGHT_THEME"
            
            # Check that colors are tuples of 4 values (RGBA)
            assert len(DARK_THEME[key]) == 4, f"DARK_THEME['{key}'] should have 4 values"
            assert len(LIGHT_THEME[key]) == 4, f"LIGHT_THEME['{key}'] should have 4 values"
            
            # Check that all color values are between 0 and 1
            for val in DARK_THEME[key]:
                assert 0 <= val <= 1, f"DARK_THEME['{key}'] value out of range"
            for val in LIGHT_THEME[key]:
                assert 0 <= val <= 1, f"LIGHT_THEME['{key}'] value out of range"
        
        # Check that light and dark themes are actually different
        assert DARK_THEME['background'] != LIGHT_THEME['background'], \
            "Dark and light theme backgrounds should be different"
        assert DARK_THEME['text'] != LIGHT_THEME['text'], \
            "Dark and light theme text colors should be different"
        
        print("✓ Theme color palette tests passed")
        return True, DARK_THEME, LIGHT_THEME
    except Exception as e:
        print(f"✗ Theme color palette tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None


def test_theme_contrast(DARK_THEME, LIGHT_THEME):
    """Test that themes have proper contrast for readability."""
    print("\nTesting theme contrast...")
    try:
        def get_brightness(color):
            """Calculate perceived brightness of a color (0-1)."""
            # Using relative luminance formula
            r, g, b = color[0], color[1], color[2]
            return 0.299 * r + 0.587 * g + 0.114 * b
        
        # Dark theme: text should be brighter than background
        dark_text_brightness = get_brightness(DARK_THEME['text'])
        dark_bg_brightness = get_brightness(DARK_THEME['background'])
        assert dark_text_brightness > dark_bg_brightness, \
            "Dark theme: text should be brighter than background"
        
        # Light theme: text should be darker than background
        light_text_brightness = get_brightness(LIGHT_THEME['text'])
        light_bg_brightness = get_brightness(LIGHT_THEME['background'])
        assert light_text_brightness < light_bg_brightness, \
            "Light theme: text should be darker than background"
        
        # Tab text should contrast with tab background
        dark_tab_text_brightness = get_brightness(DARK_THEME['tab_text'])
        dark_tab_bg_brightness = get_brightness(DARK_THEME['tab_bg'])
        contrast_ratio_dark = abs(dark_tab_text_brightness - dark_tab_bg_brightness)
        assert contrast_ratio_dark > 0.3, \
            f"Dark theme: insufficient tab text contrast ({contrast_ratio_dark:.2f})"
        
        light_tab_text_brightness = get_brightness(LIGHT_THEME['tab_text'])
        light_tab_bg_brightness = get_brightness(LIGHT_THEME['tab_bg'])
        contrast_ratio_light = abs(light_tab_text_brightness - light_tab_bg_brightness)
        assert contrast_ratio_light > 0.3, \
            f"Light theme: insufficient tab text contrast ({contrast_ratio_light:.2f})"
        
        print("✓ Theme contrast tests passed")
        return True
    except Exception as e:
        print(f"✗ Theme contrast tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all theme tests."""
    print("=" * 60)
    print("Posture Tracker - Theme Tests")
    print("=" * 60)
    
    all_passed = True
    
    # Test theme database
    if not test_theme_database():
        all_passed = False
    
    # Test theme colors (returns themes for next test)
    result, DARK_THEME, LIGHT_THEME = test_theme_colors()
    if not result:
        all_passed = False
    
    # Test theme contrast (uses themes from previous test)
    if DARK_THEME and LIGHT_THEME:
        if not test_theme_contrast(DARK_THEME, LIGHT_THEME):
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
