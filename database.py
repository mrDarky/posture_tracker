import sqlite3
import os
import json
from datetime import datetime


# Default settings constants
DEFAULT_TILT_THRESHOLD = 15.0  # degrees
DEFAULT_CAMERA_INDEX = 0  # default camera
DEFAULT_THEME = 'dark'  # default theme: 'dark' or 'light'


class SettingsDatabase:
    """Database handler for storing application settings."""
    
    def __init__(self, db_path='posture_settings.db'):
        """Initialize database connection and create tables if needed."""
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Create settings and training tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        # Current workout table (exercises in current training session)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS current_workout (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise_id TEXT NOT NULL,
                sets INTEGER DEFAULT 3,
                reps INTEGER DEFAULT 10,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Workout history table (completed workouts)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workout_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise_id TEXT NOT NULL,
                sets_completed INTEGER,
                reps_completed INTEGER,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_setting(self, key, default=None):
        """Retrieve a setting value by key."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else default
    
    def set_setting(self, key, value):
        """Store or update a setting value."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        ''', (key, value))
        conn.commit()
        conn.close()
    
    def get_tilt_threshold(self):
        """Get the tilt threshold setting (default: 15 degrees)."""
        return float(self.get_setting('tilt_threshold', str(DEFAULT_TILT_THRESHOLD)))
    
    def set_tilt_threshold(self, value):
        """Set the tilt threshold setting."""
        self.set_setting('tilt_threshold', str(value))
    
    def get_default_camera(self):
        """Get the default camera index setting (default: 0)."""
        return int(self.get_setting('default_camera', str(DEFAULT_CAMERA_INDEX)))
    
    def set_default_camera(self, value):
        """Set the default camera index setting."""
        self.set_setting('default_camera', str(value))
    
    def get_theme(self):
        """Get the theme setting (default: 'dark')."""
        return self.get_setting('theme', DEFAULT_THEME)
    
    def set_theme(self, value):
        """Set the theme setting ('dark' or 'light')."""
        if value not in ['dark', 'light']:
            raise ValueError("Theme must be 'dark' or 'light'")
        self.set_setting('theme', value)
    
    # ===== Training/Workout Methods =====
    
    def add_exercise_to_workout(self, exercise_id, sets=3, reps=10):
        """Add an exercise to current workout."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO current_workout (exercise_id, sets, reps)
            VALUES (?, ?, ?)
        ''', (exercise_id, sets, reps))
        conn.commit()
        conn.close()
    
    def remove_exercise_from_workout(self, workout_id):
        """Remove an exercise from current workout."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM current_workout WHERE id = ?', (workout_id,))
        conn.commit()
        conn.close()
    
    def get_current_workout(self):
        """Get all exercises in current workout."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, exercise_id, sets, reps, added_date FROM current_workout ORDER BY added_date')
        results = cursor.fetchall()
        conn.close()
        
        workout = []
        for row in results:
            workout.append({
                'id': row[0],
                'exercise_id': row[1],
                'sets': row[2],
                'reps': row[3],
                'added_date': row[4]
            })
        return workout
    
    def clear_current_workout(self):
        """Clear all exercises from current workout."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM current_workout')
        conn.commit()
        conn.close()
    
    def update_workout_exercise(self, workout_id, sets=None, reps=None):
        """Update sets/reps for an exercise in current workout."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if sets is not None:
            cursor.execute('UPDATE current_workout SET sets = ? WHERE id = ?', (sets, workout_id))
        if reps is not None:
            cursor.execute('UPDATE current_workout SET reps = ? WHERE id = ?', (reps, workout_id))
        
        conn.commit()
        conn.close()
    
    def save_workout_to_history(self, exercise_id, sets_completed, reps_completed, notes=''):
        """Save completed workout to history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO workout_history (exercise_id, sets_completed, reps_completed, notes)
            VALUES (?, ?, ?, ?)
        ''', (exercise_id, sets_completed, reps_completed, notes))
        conn.commit()
        conn.close()
    
    def get_workout_history(self, limit=50):
        """Get workout history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, exercise_id, sets_completed, reps_completed, date, notes
            FROM workout_history
            ORDER BY date DESC
            LIMIT ?
        ''', (limit,))
        results = cursor.fetchall()
        conn.close()
        
        history = []
        for row in results:
            history.append({
                'id': row[0],
                'exercise_id': row[1],
                'sets_completed': row[2],
                'reps_completed': row[3],
                'date': row[4],
                'notes': row[5]
            })
        return history
