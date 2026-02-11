import sqlite3
import os


# Default settings constants
DEFAULT_TILT_THRESHOLD = 15.0  # degrees
DEFAULT_CAMERA_INDEX = 0  # default camera


class SettingsDatabase:
    """Database handler for storing application settings."""
    
    def __init__(self, db_path='posture_settings.db'):
        """Initialize database connection and create tables if needed."""
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Create settings table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
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
