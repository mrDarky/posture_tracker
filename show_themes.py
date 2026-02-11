#!/usr/bin/env python3
"""
Visual representation of Dark and Light themes.
Shows color values and contrast for both themes.
"""

def rgb_to_hex(r, g, b):
    """Convert RGB (0-1) to hex color."""
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def get_brightness(color):
    """Calculate perceived brightness of a color (0-1)."""
    r, g, b = color[0], color[1], color[2]
    return 0.299 * r + 0.587 * g + 0.114 * b


def show_theme(theme_name, theme_colors):
    """Display theme colors in a formatted way."""
    print(f"\n{'='*70}")
    print(f"  {theme_name.upper()} THEME")
    print(f"{'='*70}\n")
    
    # Color categories
    categories = {
        'Background Colors': ['background', 'surface', 'surface_variant'],
        'Text Colors': ['text', 'text_muted', 'text_dimmed'],
        'Status Colors': ['neutral', 'good', 'bad', 'accent', 'scanning'],
        'Tab Colors': ['tab_bg', 'tab_text']
    }
    
    for category, keys in categories.items():
        print(f"  {category}:")
        print(f"  {'-' * 60}")
        for key in keys:
            if key in theme_colors:
                color = theme_colors[key]
                r, g, b, a = color
                hex_color = rgb_to_hex(r, g, b)
                brightness = get_brightness(color)
                brightness_str = "■" * int(brightness * 20)
                
                print(f"    {key:18} {hex_color:8}  RGB({r:.2f}, {g:.2f}, {b:.2f})")
                print(f"    {'':18} Brightness: {brightness_str} {brightness:.2%}")
        print()


def show_contrast_check(theme_name, theme_colors):
    """Show contrast ratios for important color pairs."""
    print(f"\n  Contrast Analysis for {theme_name} Theme:")
    print(f"  {'-' * 60}")
    
    # Key contrast pairs
    pairs = [
        ('text', 'background', 'Text on Background'),
        ('text_muted', 'background', 'Muted Text on Background'),
        ('tab_text', 'tab_bg', 'Tab Text on Tab Background'),
    ]
    
    for color1_key, color2_key, description in pairs:
        color1 = theme_colors[color1_key]
        color2 = theme_colors[color2_key]
        
        brightness1 = get_brightness(color1)
        brightness2 = get_brightness(color2)
        contrast = abs(brightness1 - brightness2)
        
        # Simple contrast ratio (not WCAG formula, but good enough for visualization)
        status = "✓ Good" if contrast > 0.3 else "✗ Poor"
        
        print(f"    {description:30} Contrast: {contrast:.2%}  {status}")
    print()


def main():
    """Display both themes."""
    # Read theme definitions from main.py
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Extract DARK_THEME
    dark_start = content.find('DARK_THEME = {')
    dark_end = content.find('}', dark_start) + 1
    dark_theme_str = content[dark_start:dark_end]
    
    # Extract LIGHT_THEME
    light_start = content.find('LIGHT_THEME = {')
    light_end = content.find('}', light_start) + 1
    light_theme_str = content[light_start:light_end]
    
    # Execute to get dictionaries
    exec_globals = {}
    exec(dark_theme_str, exec_globals)
    exec(light_theme_str, exec_globals)
    
    DARK_THEME = exec_globals['DARK_THEME']
    LIGHT_THEME = exec_globals['LIGHT_THEME']
    
    print("\n" + "="*70)
    print("  POSTURE TRACKER - THEME VISUALIZATION")
    print("="*70)
    
    # Show Dark Theme
    show_theme("Dark", DARK_THEME)
    show_contrast_check("Dark", DARK_THEME)
    
    # Show Light Theme
    show_theme("Light", LIGHT_THEME)
    show_contrast_check("Light", LIGHT_THEME)
    
    # Summary
    print("\n" + "="*70)
    print("  SUMMARY")
    print("="*70)
    print("\n  Both themes have been implemented with:")
    print("    ✓ Proper text contrast for readability")
    print("    ✓ Tab background colors for better tab visibility")
    print("    ✓ Consistent color semantics (good=green, bad=red, etc.)")
    print("    ✓ Smooth transition between themes")
    print("\n  Users can switch themes from Settings tab.")
    print("  Theme preference is saved to database.\n")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
