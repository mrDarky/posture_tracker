#!/usr/bin/env python3
"""
Test to verify the default tab fix.
When do_default_tab is True, Kivy's TabbedPanel creates an empty 'Default' tab
that is shown on startup, resulting in a grey screen with no content.
Setting do_default_tab to False makes the first TabbedPanelItem (Camera) the default.
"""

import sys


def test_do_default_tab_is_false():
    """Test that do_default_tab is set to False in the .kv file."""
    print("Testing do_default_tab setting...")

    with open('posture_tracker.kv', 'r') as f:
        content = f.read()

    if "do_default_tab: False" in content:
        print("  ✓ do_default_tab is False (Camera tab shown on startup)")
    else:
        print("  ✗ do_default_tab should be False to avoid empty grey screen")
        return False

    if "do_default_tab: True" in content:
        print("  ✗ do_default_tab: True found — this causes an empty default tab")
        return False

    return True


def test_camera_tab_is_first():
    """Test that the Camera tab is the first TabbedPanelItem."""
    print("\nTesting Camera tab position...")

    with open('posture_tracker.kv', 'r') as f:
        content = f.read()

    # Find positions of TabbedPanelItem declarations
    lines = content.split('\n')
    tab_items = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('TabbedPanelItem:'):
            tab_items.append(i)
        if stripped.startswith("text: 'Camera'") and tab_items:
            # Verify Camera is associated with the first TabbedPanelItem
            if len(tab_items) == 1:
                print("  ✓ Camera tab is the first TabbedPanelItem")
                return True

    print("  ✗ Camera tab should be the first TabbedPanelItem")
    return False


def main():
    """Run all default tab fix tests."""
    print("=" * 60)
    print("Default Tab Fix - Verification")
    print("=" * 60)
    print()

    all_passed = True

    if not test_do_default_tab_is_false():
        all_passed = False

    if not test_camera_tab_is_first():
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("All default tab fix checks PASSED ✓")
        return 0
    else:
        print("Some default tab fix checks FAILED ✗")
        return 1


if __name__ == '__main__':
    sys.exit(main())
