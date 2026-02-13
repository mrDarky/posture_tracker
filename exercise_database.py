"""
Exercise database containing all available exercises with their definitions.
Each exercise includes name, description, target muscles, difficulty, and form checking criteria.
"""

# Exercise categories
CATEGORY_BODYWEIGHT = "Bodyweight"
CATEGORY_DUMBBELLS = "Dumbbells"
CATEGORY_STRETCHING = "Stretching"

# Difficulty levels
DIFFICULTY_BEGINNER = "Beginner"
DIFFICULTY_INTERMEDIATE = "Intermediate"
DIFFICULTY_ADVANCED = "Advanced"


class Exercise:
    """Represents a single exercise."""
    
    def __init__(self, exercise_id, name, category, difficulty, description, 
                 target_muscles, instructions, form_checks=None):
        """
        Initialize an exercise.
        
        Args:
            exercise_id: Unique identifier for the exercise
            name: Exercise name
            category: Exercise category (bodyweight, dumbbells, etc.)
            difficulty: Difficulty level (beginner, intermediate, advanced)
            description: Brief description of the exercise
            target_muscles: List of target muscle groups
            instructions: Step-by-step instructions
            form_checks: Dictionary of form checking criteria for camera validation
        """
        self.id = exercise_id
        self.name = name
        self.category = category
        self.difficulty = difficulty
        self.description = description
        self.target_muscles = target_muscles
        self.instructions = instructions
        self.form_checks = form_checks or {}
    
    def to_dict(self):
        """Convert exercise to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'difficulty': self.difficulty,
            'description': self.description,
            'target_muscles': self.target_muscles,
            'instructions': self.instructions,
            'form_checks': self.form_checks,
        }


# Complete exercise database
EXERCISES = [
    # ===== BODYWEIGHT EXERCISES =====
    Exercise(
        exercise_id='pushup',
        name='Push-ups',
        category=CATEGORY_BODYWEIGHT,
        difficulty=DIFFICULTY_BEGINNER,
        description='Classic upper body exercise targeting chest, shoulders, and triceps',
        target_muscles=['Chest', 'Shoulders', 'Triceps', 'Core'],
        instructions=[
            'Start in plank position with hands shoulder-width apart',
            'Keep your body in a straight line from head to heels',
            'Lower your body until chest nearly touches the floor',
            'Push back up to starting position',
            'Keep elbows at 45-degree angle to body'
        ],
        form_checks={
            'elbow_angle_min': 70,
            'elbow_angle_max': 110,
            'body_alignment': 'straight',
            'shoulder_width': 'standard'
        }
    ),
    Exercise(
        exercise_id='pullup',
        name='Pull-ups',
        category=CATEGORY_BODYWEIGHT,
        difficulty=DIFFICULTY_INTERMEDIATE,
        description='Upper body pulling exercise targeting back and biceps',
        target_muscles=['Back', 'Biceps', 'Shoulders', 'Core'],
        instructions=[
            'Hang from bar with palms facing away, hands shoulder-width apart',
            'Pull yourself up until chin is over the bar',
            'Lower yourself back down with control',
            'Keep core engaged throughout movement',
            'Avoid swinging or kipping'
        ],
        form_checks={
            'elbow_angle_min': 30,
            'elbow_angle_max': 180,
            'shoulder_elevation': 'full',
            'body_swing': 'minimal'
        }
    ),
    Exercise(
        exercise_id='squat',
        name='Squats',
        category=CATEGORY_BODYWEIGHT,
        difficulty=DIFFICULTY_BEGINNER,
        description='Fundamental lower body exercise targeting legs and glutes',
        target_muscles=['Quadriceps', 'Glutes', 'Hamstrings', 'Core'],
        instructions=[
            'Stand with feet shoulder-width apart',
            'Lower your body by bending knees and hips',
            'Keep chest up and back straight',
            'Lower until thighs are parallel to ground',
            'Push through heels to return to standing'
        ],
        form_checks={
            'knee_angle_min': 80,
            'knee_angle_max': 100,
            'back_angle': 'neutral',
            'knee_alignment': 'over_toes'
        }
    ),
    Exercise(
        exercise_id='lunges',
        name='Lunges',
        category=CATEGORY_BODYWEIGHT,
        difficulty=DIFFICULTY_BEGINNER,
        description='Single-leg exercise for lower body strength and balance',
        target_muscles=['Quadriceps', 'Glutes', 'Hamstrings', 'Calves'],
        instructions=[
            'Stand with feet hip-width apart',
            'Step forward with one leg',
            'Lower body until both knees are at 90 degrees',
            'Push back to starting position',
            'Alternate legs'
        ],
        form_checks={
            'front_knee_angle': 90,
            'back_knee_angle': 90,
            'torso_upright': True,
            'knee_over_ankle': True
        }
    ),
    Exercise(
        exercise_id='plank',
        name='Plank',
        category=CATEGORY_BODYWEIGHT,
        difficulty=DIFFICULTY_BEGINNER,
        description='Isometric core strengthening exercise',
        target_muscles=['Core', 'Shoulders', 'Back'],
        instructions=[
            'Start on forearms and toes',
            'Keep body in straight line from head to heels',
            'Engage core and squeeze glutes',
            'Hold position without sagging or raising hips',
            'Breathe steadily'
        ],
        form_checks={
            'body_alignment': 'straight',
            'hip_position': 'neutral',
            'shoulder_stability': True
        }
    ),
    Exercise(
        exercise_id='burpees',
        name='Burpees',
        category=CATEGORY_BODYWEIGHT,
        difficulty=DIFFICULTY_INTERMEDIATE,
        description='Full body exercise combining push-up and jump',
        target_muscles=['Full Body', 'Cardio'],
        instructions=[
            'Start standing',
            'Drop into squat position with hands on ground',
            'Kick feet back into push-up position',
            'Perform push-up',
            'Jump feet back to squat',
            'Jump up with arms overhead'
        ],
        form_checks={
            'full_extension': True,
            'push_up_depth': 'chest_to_floor',
            'jump_height': 'minimal'
        }
    ),
    Exercise(
        exercise_id='mountain_climbers',
        name='Mountain Climbers',
        category=CATEGORY_BODYWEIGHT,
        difficulty=DIFFICULTY_BEGINNER,
        description='Dynamic core and cardio exercise',
        target_muscles=['Core', 'Shoulders', 'Hip Flexors', 'Cardio'],
        instructions=[
            'Start in push-up position',
            'Bring one knee toward chest',
            'Quickly switch legs',
            'Keep core tight and hips level',
            'Maintain steady rhythm'
        ],
        form_checks={
            'hip_level': True,
            'pace': 'steady',
            'knee_drive': 'full'
        }
    ),
    Exercise(
        exercise_id='dips',
        name='Dips',
        category=CATEGORY_BODYWEIGHT,
        difficulty=DIFFICULTY_INTERMEDIATE,
        description='Upper body exercise targeting triceps and chest',
        target_muscles=['Triceps', 'Chest', 'Shoulders'],
        instructions=[
            'Support yourself on parallel bars or bench',
            'Lower body by bending elbows',
            'Keep elbows close to body',
            'Lower until upper arms are parallel to ground',
            'Push back up to starting position'
        ],
        form_checks={
            'elbow_angle_min': 80,
            'elbow_angle_max': 100,
            'torso_lean': 'slight_forward',
            'shoulder_position': 'down'
        }
    ),
    
    # ===== DUMBBELL EXERCISES =====
    Exercise(
        exercise_id='dumbbell_press',
        name='Dumbbell Shoulder Press',
        category=CATEGORY_DUMBBELLS,
        difficulty=DIFFICULTY_BEGINNER,
        description='Overhead pressing exercise for shoulders',
        target_muscles=['Shoulders', 'Triceps', 'Upper Chest'],
        instructions=[
            'Stand or sit with dumbbells at shoulder height',
            'Press dumbbells overhead until arms are extended',
            'Lower with control back to shoulder height',
            'Keep core engaged',
            'Avoid arching lower back'
        ],
        form_checks={
            'elbow_angle_bottom': 90,
            'arm_extension_top': True,
            'back_arch': 'minimal',
            'dumbbell_path': 'vertical'
        }
    ),
    Exercise(
        exercise_id='dumbbell_curl',
        name='Dumbbell Bicep Curl',
        category=CATEGORY_DUMBBELLS,
        difficulty=DIFFICULTY_BEGINNER,
        description='Isolation exercise for biceps',
        target_muscles=['Biceps', 'Forearms'],
        instructions=[
            'Stand with dumbbells at sides, palms forward',
            'Curl weights up toward shoulders',
            'Keep elbows stationary at sides',
            'Lower with control',
            'Avoid swinging or using momentum'
        ],
        form_checks={
            'elbow_position': 'fixed',
            'curl_angle_top': 45,
            'body_swing': 'none',
            'controlled_descent': True
        }
    ),
    Exercise(
        exercise_id='dumbbell_row',
        name='Dumbbell Bent-Over Row',
        category=CATEGORY_DUMBBELLS,
        difficulty=DIFFICULTY_INTERMEDIATE,
        description='Back exercise for upper and middle back',
        target_muscles=['Back', 'Biceps', 'Rear Shoulders'],
        instructions=[
            'Bend at hips with flat back, dumbbells hanging down',
            'Pull dumbbells to sides of torso',
            'Squeeze shoulder blades together',
            'Lower with control',
            'Keep back flat throughout'
        ],
        form_checks={
            'back_angle': 'flat',
            'elbow_path': 'close_to_body',
            'shoulder_retraction': True,
            'torso_stable': True
        }
    ),
    Exercise(
        exercise_id='dumbbell_goblet_squat',
        name='Goblet Squat',
        category=CATEGORY_DUMBBELLS,
        difficulty=DIFFICULTY_BEGINNER,
        description='Squat variation holding dumbbell at chest',
        target_muscles=['Quadriceps', 'Glutes', 'Core'],
        instructions=[
            'Hold dumbbell at chest with both hands',
            'Stand with feet shoulder-width apart',
            'Squat down keeping chest up',
            'Lower until thighs parallel to ground',
            'Push through heels to stand'
        ],
        form_checks={
            'dumbbell_position': 'chest',
            'squat_depth': 'parallel',
            'chest_up': True,
            'knee_alignment': True
        }
    ),
    Exercise(
        exercise_id='dumbbell_lunge',
        name='Dumbbell Lunges',
        category=CATEGORY_DUMBBELLS,
        difficulty=DIFFICULTY_INTERMEDIATE,
        description='Weighted lunge for lower body',
        target_muscles=['Quadriceps', 'Glutes', 'Hamstrings'],
        instructions=[
            'Hold dumbbells at sides',
            'Step forward into lunge position',
            'Lower until both knees at 90 degrees',
            'Push back to starting position',
            'Keep torso upright'
        ],
        form_checks={
            'front_knee_angle': 90,
            'back_knee_angle': 90,
            'torso_upright': True,
            'balance_stable': True
        }
    ),
    Exercise(
        exercise_id='dumbbell_deadlift',
        name='Dumbbell Deadlift',
        category=CATEGORY_DUMBBELLS,
        difficulty=DIFFICULTY_INTERMEDIATE,
        description='Hip hinge movement for posterior chain',
        target_muscles=['Hamstrings', 'Glutes', 'Lower Back', 'Core'],
        instructions=[
            'Stand with dumbbells in front of thighs',
            'Hinge at hips pushing butt back',
            'Lower dumbbells along legs',
            'Keep back flat and chest up',
            'Drive hips forward to stand'
        ],
        form_checks={
            'back_flat': True,
            'hip_hinge': True,
            'knee_slight_bend': True,
            'weight_path': 'close_to_legs'
        }
    ),
    Exercise(
        exercise_id='dumbbell_chest_press',
        name='Dumbbell Chest Press',
        category=CATEGORY_DUMBBELLS,
        difficulty=DIFFICULTY_BEGINNER,
        description='Pressing exercise for chest on bench',
        target_muscles=['Chest', 'Shoulders', 'Triceps'],
        instructions=[
            'Lie on bench with dumbbells at chest level',
            'Press dumbbells up until arms extended',
            'Lower with control to chest level',
            'Keep shoulder blades retracted',
            'Maintain stable position'
        ],
        form_checks={
            'press_path': 'vertical',
            'elbow_angle_bottom': 90,
            'arm_extension_top': True,
            'scapula_retracted': True
        }
    ),
    Exercise(
        exercise_id='dumbbell_lateral_raise',
        name='Lateral Raises',
        category=CATEGORY_DUMBBELLS,
        difficulty=DIFFICULTY_BEGINNER,
        description='Shoulder isolation exercise',
        target_muscles=['Shoulders (Lateral Deltoids)'],
        instructions=[
            'Stand with dumbbells at sides',
            'Raise arms out to sides',
            'Lift until arms parallel to ground',
            'Lower with control',
            'Keep slight bend in elbows'
        ],
        form_checks={
            'arm_height': 'shoulder_level',
            'elbow_bend': 'slight',
            'torso_stable': True,
            'controlled_motion': True
        }
    ),
    Exercise(
        exercise_id='dumbbell_tricep_extension',
        name='Overhead Tricep Extension',
        category=CATEGORY_DUMBBELLS,
        difficulty=DIFFICULTY_BEGINNER,
        description='Isolation exercise for triceps',
        target_muscles=['Triceps'],
        instructions=[
            'Hold dumbbell overhead with both hands',
            'Lower dumbbell behind head by bending elbows',
            'Keep upper arms stationary',
            'Extend arms back to starting position',
            'Keep core engaged'
        ],
        form_checks={
            'upper_arm_vertical': True,
            'elbow_position': 'fixed',
            'full_extension': True,
            'core_stable': True
        }
    ),
    Exercise(
        exercise_id='dumbbell_arnold_press',
        name='Arnold Press',
        category=CATEGORY_DUMBBELLS,
        difficulty=DIFFICULTY_ADVANCED,
        description='Rotational shoulder press exercise',
        target_muscles=['Shoulders', 'Triceps'],
        instructions=[
            'Start with dumbbells at shoulder height, palms facing you',
            'Rotate palms forward while pressing overhead',
            'Fully extend arms',
            'Reverse motion to return',
            'Keep core tight'
        ],
        form_checks={
            'rotation_smooth': True,
            'press_path': 'curved',
            'full_extension': True,
            'control': True
        }
    ),
    
    # ===== STRETCHING EXERCISES =====
    Exercise(
        exercise_id='hamstring_stretch',
        name='Hamstring Stretch',
        category=CATEGORY_STRETCHING,
        difficulty=DIFFICULTY_BEGINNER,
        description='Stretches the back of thighs',
        target_muscles=['Hamstrings'],
        instructions=[
            'Sit on floor with legs extended',
            'Reach forward toward toes',
            'Keep back straight',
            'Hold for 20-30 seconds',
            'Breathe deeply and relax'
        ],
        form_checks={
            'back_straight': True,
            'legs_extended': True,
            'reach_depth': 'comfortable'
        }
    ),
    Exercise(
        exercise_id='quad_stretch',
        name='Quadriceps Stretch',
        category=CATEGORY_STRETCHING,
        difficulty=DIFFICULTY_BEGINNER,
        description='Stretches front of thigh',
        target_muscles=['Quadriceps'],
        instructions=[
            'Stand on one leg',
            'Grab opposite foot behind you',
            'Pull heel toward glutes',
            'Keep knees together',
            'Hold for 20-30 seconds each side'
        ],
        form_checks={
            'balance_stable': True,
            'knee_alignment': True,
            'upright_posture': True
        }
    ),
    Exercise(
        exercise_id='chest_doorway_stretch',
        name='Chest Doorway Stretch',
        category=CATEGORY_STRETCHING,
        difficulty=DIFFICULTY_BEGINNER,
        description='Opens up chest and shoulders',
        target_muscles=['Chest', 'Shoulders'],
        instructions=[
            'Stand in doorway with arm on door frame',
            'Step forward with one foot',
            'Lean forward gently',
            'Feel stretch in chest',
            'Hold 20-30 seconds each side'
        ],
        form_checks={
            'arm_position': '90_degrees',
            'lean_depth': 'moderate',
            'shoulder_safe': True
        }
    ),
    Exercise(
        exercise_id='shoulder_stretch',
        name='Cross-Body Shoulder Stretch',
        category=CATEGORY_STRETCHING,
        difficulty=DIFFICULTY_BEGINNER,
        description='Stretches shoulder and upper back',
        target_muscles=['Shoulders', 'Upper Back'],
        instructions=[
            'Bring one arm across body',
            'Use other arm to pull it closer',
            'Keep shoulders down',
            'Hold 20-30 seconds',
            'Repeat other side'
        ],
        form_checks={
            'arm_straight': True,
            'shoulders_down': True,
            'gentle_pull': True
        }
    ),
    Exercise(
        exercise_id='cat_cow_stretch',
        name='Cat-Cow Stretch',
        category=CATEGORY_STRETCHING,
        difficulty=DIFFICULTY_BEGINNER,
        description='Dynamic spine mobility stretch',
        target_muscles=['Spine', 'Core', 'Back'],
        instructions=[
            'Start on hands and knees',
            'Arch back and look up (cow)',
            'Round back and tuck chin (cat)',
            'Alternate slowly',
            'Repeat 10-15 times'
        ],
        form_checks={
            'full_range': True,
            'smooth_movement': True,
            'neck_alignment': True
        }
    ),
    Exercise(
        exercise_id='hip_flexor_stretch',
        name='Hip Flexor Stretch',
        category=CATEGORY_STRETCHING,
        difficulty=DIFFICULTY_BEGINNER,
        description='Stretches front of hip',
        target_muscles=['Hip Flexors', 'Quadriceps'],
        instructions=[
            'Kneel on one knee',
            'Other foot forward in lunge position',
            'Push hips forward',
            'Keep torso upright',
            'Hold 20-30 seconds each side'
        ],
        form_checks={
            'upright_torso': True,
            'hip_forward': True,
            'back_knee_down': True
        }
    ),
]


class ExerciseDatabase:
    """Manager for exercise database operations."""
    
    def __init__(self):
        """Initialize exercise database."""
        self.exercises = {ex.id: ex for ex in EXERCISES}
    
    def get_all_exercises(self):
        """Get all exercises."""
        return list(self.exercises.values())
    
    def get_exercise_by_id(self, exercise_id):
        """Get specific exercise by ID."""
        return self.exercises.get(exercise_id)
    
    def get_exercises_by_category(self, category):
        """Get all exercises in a category."""
        return [ex for ex in self.exercises.values() if ex.category == category]
    
    def get_exercises_by_difficulty(self, difficulty):
        """Get all exercises of a difficulty level."""
        return [ex for ex in self.exercises.values() if ex.difficulty == difficulty]
    
    def get_categories(self):
        """Get list of all categories."""
        return list(set(ex.category for ex in self.exercises.values()))
    
    def search_exercises(self, query):
        """Search exercises by name or description."""
        query = query.lower()
        return [ex for ex in self.exercises.values() 
                if query in ex.name.lower() or query in ex.description.lower()]
