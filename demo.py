#!/usr/bin/env python3
"""
Demo script to show how the posture tracker works.
This simulates the posture detection logic without requiring a camera.
"""

import time
from database import SettingsDatabase

def demo_settings_persistence():
    """Demonstrate settings persistence."""
    print("=" * 60)
    print("DEMO: Settings Persistence")
    print("=" * 60)
    
    # Create database
    db = SettingsDatabase('demo_settings.db')
    
    print("\n1. Setting tilt threshold to 20 degrees...")
    db.set_tilt_threshold(20.0)
    
    print("2. Reading back the threshold...")
    threshold = db.get_tilt_threshold()
    print(f"   Current threshold: {threshold} degrees")
    
    print("\n3. Changing threshold to 15 degrees...")
    db.set_tilt_threshold(15.0)
    
    print("4. Reading back the threshold again...")
    threshold = db.get_tilt_threshold()
    print(f"   Current threshold: {threshold} degrees")
    
    print("\n✓ Settings are persistent and working correctly!")
    
    # Clean up demo database
    import os
    if os.path.exists('demo_settings.db'):
        os.remove('demo_settings.db')

def demo_posture_detection():
    """Demonstrate posture detection logic."""
    print("\n" + "=" * 60)
    print("DEMO: Posture Detection Logic")
    print("=" * 60)
    
    import math
    
    def calculate_tilt(left_shoulder, right_shoulder):
        """Calculate shoulder tilt angle."""
        x_diff = right_shoulder[0] - left_shoulder[0]
        y_diff = right_shoulder[1] - left_shoulder[1]
        angle = math.degrees(math.atan2(y_diff, x_diff))
        return abs(angle)
    
    # Simulate different postures
    scenarios = [
        {
            'name': 'Good Posture (level shoulders)',
            'left': (100, 100),
            'right': (200, 100),
            'threshold': 15.0
        },
        {
            'name': 'Slight Tilt (10 degrees)',
            'left': (100, 100),
            'right': (200, 117.6),  # Creates ~10 degree tilt
            'threshold': 15.0
        },
        {
            'name': 'Bad Posture (20 degrees)',
            'left': (100, 100),
            'right': (200, 136.4),  # Creates ~20 degree tilt
            'threshold': 15.0
        }
    ]
    
    print("\nSimulating different posture scenarios:\n")
    
    for scenario in scenarios:
        tilt = calculate_tilt(scenario['left'], scenario['right'])
        threshold = scenario['threshold']
        is_bad = tilt > threshold
        
        print(f"Scenario: {scenario['name']}")
        print(f"  Left shoulder:  {scenario['left']}")
        print(f"  Right shoulder: {scenario['right']}")
        print(f"  Tilt angle:     {tilt:.1f}°")
        print(f"  Threshold:      {threshold}°")
        print(f"  Status:         {'❌ BAD POSTURE' if is_bad else '✓ Good posture'}")
        print()

def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("POSTURE TRACKER - DEMONSTRATION")
    print("=" * 60)
    print("\nThis demo shows how the posture tracker works")
    print("without requiring a camera or GUI.\n")
    
    time.sleep(1)
    
    demo_settings_persistence()
    time.sleep(1)
    
    demo_posture_detection()
    
    print("=" * 60)
    print("\nTo run the full application with camera:")
    print("  python main.py")
    print("\nMake sure you have installed all dependencies:")
    print("  pip install -r requirements.txt")
    print("=" * 60)

if __name__ == '__main__':
    main()
