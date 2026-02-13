# Training Tab UI Preview

## Layout Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  [Camera]  [Training]  [Settings]                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────────────────────────────┬──────────────────────────────────┐│
│  │ Exercise: [Push-ups ▼]               │ Category: [All ▼]                ││
│  └──────────────────────────────────────┴──────────────────────────────────┘│
│                                                                               │
│  ┌─────────────────────────────────────────┬───────────────────────────────┐│
│  │                                         │                               ││
│  │  ┌──────────────────────────────────┐  │  ┌─────────────────────────┐ ││
│  │  │                                  │  │  │  Exercise Details       │ ││
│  │  │    [CAMERA FEED WITH POSE        │  │  │  ─────────────────────  │ ││
│  │  │     DETECTION OVERLAY]           │  │  │                         │ ││
│  │  │                                  │  │  │  Push-ups               │ ││
│  │  │    • Body landmarks visible      │  │  │  Category: Bodyweight   │ ││
│  │  │    • Rep count displayed         │  │  │  Difficulty: Beginner   │ ││
│  │  │    • Form feedback shown         │  │  │                         │ ││
│  │  │                                  │  │  │  Description:           │ ││
│  │  │                                  │  │  │  Classic upper body...  │ ││
│  │  └──────────────────────────────────┘  │  │                         │ ││
│  │                                         │  │  Target Muscles:        │ ││
│  │  ┌──────────────────────────────────┐  │  │  • Chest                │ ││
│  │  │  Reps: 12   Good form!           │  │  │  • Shoulders            │ ││
│  │  └──────────────────────────────────┘  │  │  • Triceps              │ ││
│  │                                         │  │  • Core                 │ ││
│  │  ┌───────┬────────┬────────┐          │  │                         │ ││
│  │  │ Start │  Stop  │ Reset  │          │  │  Instructions:          │ ││
│  │  └───────┴────────┴────────┘          │  │  1. Start in plank...   │ ││
│  │     (Green) (Red)  (Blue)              │  │  2. Keep body...        │ ││
│  │                                         │  │  3. Lower until...      │ ││
│  └─────────────────────────────────────────┤  └─────────────────────────┘ ││
│                                             │                               ││
│                                             │  ┌─────────────────────────┐ ││
│                                             │  │ Current Workout [+][X]  │ ││
│                                             │  │  ─────────────────────  │ ││
│                                             │  │                         │ ││
│                                             │  │  • Push-ups    3x10 [✕] │ ││
│                                             │  │  • Squats      4x12 [✕] │ ││
│                                             │  │  • Plank       3x30s[✕] │ ││
│                                             │  │                         │ ││
│                                             │  │                         │ ││
│                                             │  └─────────────────────────┘ ││
│                                             │                               ││
│                                             └───────────────────────────────┘│
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Features Visible in UI

### Header Section
- **Exercise Dropdown**: Select from 24+ exercises
- **Category Filter**: Filter by All, Bodyweight, Dumbbells, or Stretching

### Left Panel (60% width) - Camera Feed
- **Live Video Display**: Shows webcam feed with MediaPipe pose overlay
- **Status Bar**: Shows rep count and real-time form feedback
- **Control Buttons**:
  - Start (Green): Begin exercise tracking
  - Stop (Red): End exercise tracking
  - Reset (Blue): Reset rep counter

### Right Panel (40% width) - Info & Workout
- **Exercise Details Card** (top half):
  - Exercise name, category, difficulty
  - Description
  - Target muscles
  - Step-by-step instructions
  - Scrollable content

- **Current Workout Card** (bottom half):
  - + button to add current exercise
  - Clear button to remove all exercises
  - List of workout exercises with sets/reps
  - ✕ button on each item to remove individual exercises

## Color Scheme (Dark Theme)
- Background: Dark gray (#1F1F24)
- Cards: Medium gray (#2B2B33)
- Text: Light gray/white (#EDEDF2)
- Accent: Blue (#408BFF)
- Good status: Green (#2ECC71)
- Bad status: Red (#E84C3D)

## Interaction Flow

1. User selects category (optional)
2. User selects exercise from dropdown
3. Exercise details appear in right panel
4. User clicks "Start Exercise"
5. Camera feed shows with pose detection
6. Rep counter updates automatically
7. Form feedback displays in real-time
8. User can add exercise to workout using + button
9. Workout list shows all added exercises
10. User can remove exercises or clear entire workout

## Form Checking Examples

### Push-ups
- Monitors elbow angle (70-110 degrees)
- Checks body alignment
- Counts reps when going from up to down position
- Feedback: "Keep body straight", "Good depth!"

### Squats
- Monitors knee angle (80-100 degrees)
- Checks back position
- Counts reps when standing up from squat
- Feedback: "Go deeper", "Great depth!", "Keep chest up"

### Plank
- Checks body alignment (straight line)
- Monitors hip position
- No rep counting (isometric hold)
- Feedback: "Perfect alignment!", "Hips too low", "Hips too high"

## Exercise Categories Preview

### Bodyweight (8 exercises)
Push-ups, Pull-ups, Squats, Lunges, Planks, Burpees, Mountain Climbers, Dips

### Dumbbells (10 exercises)
Shoulder Press, Bicep Curls, Bent-Over Rows, Goblet Squats, Lunges, Deadlifts,
Chest Press, Lateral Raises, Tricep Extensions, Arnold Press

### Stretching (6 exercises)
Hamstring Stretch, Quad Stretch, Chest Stretch, Shoulder Stretch, 
Cat-Cow Stretch, Hip Flexor Stretch
