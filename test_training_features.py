#!/usr/bin/env python
"""
Test script to verify that the Training tab features work correctly.
Tests exercise database, detector, and database workout functions.
"""

import sys
import os
import tempfile

print("=" * 60)
print("Testing Training Tab Features")
print("=" * 60)

try:
    # Test 1: Exercise Database
    print("\n1. Testing Exercise Database...")
    from exercise_database import ExerciseDatabase, CATEGORY_BODYWEIGHT, CATEGORY_DUMBBELLS
    
    ex_db = ExerciseDatabase()
    
    # Check total exercises
    all_exercises = ex_db.get_all_exercises()
    assert len(all_exercises) > 0, "No exercises found"
    print(f"   ✓ Loaded {len(all_exercises)} exercises")
    
    # Check categories
    categories = ex_db.get_categories()
    assert len(categories) > 0, "No categories found"
    print(f"   ✓ Found {len(categories)} categories: {categories}")
    
    # Check specific exercise
    pushup = ex_db.get_exercise_by_id('pushup')
    assert pushup is not None, "Push-up exercise not found"
    assert pushup.name == 'Push-ups', "Push-up name incorrect"
    print(f"   ✓ Found specific exercise: {pushup.name}")
    
    # Check category filtering
    bodyweight_exercises = ex_db.get_exercises_by_category(CATEGORY_BODYWEIGHT)
    assert len(bodyweight_exercises) > 0, "No bodyweight exercises found"
    print(f"   ✓ Found {len(bodyweight_exercises)} bodyweight exercises")
    
    # Test 2: Exercise Detector
    print("\n2. Testing Exercise Detector...")
    from exercise_detector import ExerciseDetector
    
    detector = ExerciseDetector()
    assert detector is not None, "Failed to create detector"
    print("   ✓ Exercise detector initialized")
    
    # Test set exercise
    detector.set_exercise('pushup')
    assert detector.current_exercise == 'pushup', "Failed to set exercise"
    print("   ✓ Set current exercise to push-up")
    
    # Test reset counter
    detector.reset_counter()
    assert detector.rep_count == 0, "Failed to reset counter"
    print("   ✓ Counter reset works")
    
    # Clean up
    detector.release()
    print("   ✓ Detector released successfully")
    
    # Test 3: Database Workout Functions
    print("\n3. Testing Database Workout Functions...")
    from database import SettingsDatabase
    
    # Create temp database
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.db') as f:
        temp_db_path = f.name
    
    try:
        db = SettingsDatabase(temp_db_path)
        
        # Test add exercise to workout
        db.add_exercise_to_workout('pushup', sets=3, reps=10)
        workout = db.get_current_workout()
        assert len(workout) == 1, "Failed to add exercise to workout"
        assert workout[0]['exercise_id'] == 'pushup', "Wrong exercise added"
        print("   ✓ Added exercise to workout")
        
        # Test add another exercise
        db.add_exercise_to_workout('squat', sets=4, reps=12)
        workout = db.get_current_workout()
        assert len(workout) == 2, "Failed to add second exercise"
        print(f"   ✓ Added second exercise (total: {len(workout)})")
        
        # Test remove exercise
        workout_id = workout[0]['id']
        db.remove_exercise_from_workout(workout_id)
        workout = db.get_current_workout()
        assert len(workout) == 1, "Failed to remove exercise"
        print("   ✓ Removed exercise from workout")
        
        # Test clear workout
        db.clear_current_workout()
        workout = db.get_current_workout()
        assert len(workout) == 0, "Failed to clear workout"
        print("   ✓ Cleared workout")
        
        # Test workout history
        db.save_workout_to_history('pushup', 3, 10, 'Great session!')
        history = db.get_workout_history(limit=10)
        assert len(history) == 1, "Failed to save to history"
        assert history[0]['exercise_id'] == 'pushup', "Wrong exercise in history"
        print("   ✓ Saved workout to history")
        
    finally:
        # Clean up temp database
        if os.path.exists(temp_db_path):
            os.unlink(temp_db_path)
    
    # Test 4: Verify main module has training methods (without GUI)
    print("\n4. Checking main module for training methods...")
    
    # Just verify the file contains the expected methods without importing
    with open('main.py', 'r') as f:
        main_content = f.read()
    
    required_methods = [
        'populate_exercise_list',
        'start_training',
        'stop_training',
        'add_current_exercise_to_workout',
        'filter_exercises_by_category',
        'select_exercise'
    ]
    
    for method in required_methods:
        assert f'def {method}' in main_content, f"{method} method not found in main.py"
    
    print(f"   ✓ All {len(required_methods)} training methods found in main.py")
    
    print("\n" + "=" * 60)
    print("SUCCESS: All training tab tests passed!")
    print("=" * 60)
    print("\nTraining tab features:")
    print(f"  • {len(all_exercises)} exercises available")
    print(f"  • {len(categories)} categories: {', '.join(categories)}")
    print("  • Exercise form detection with camera")
    print("  • Add/remove exercises to/from workout")
    print("  • Rep counting for supported exercises")
    sys.exit(0)
    
except Exception as e:
    print(f"\n{'=' * 60}")
    print(f"FAILED: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
    sys.exit(1)
