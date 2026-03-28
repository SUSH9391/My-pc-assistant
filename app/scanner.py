import sqlite3
import os
import time
import psutil
from pathlib import Path
from loguru import logger

# Note: Ensure app.config and app.utils exist in your structure
try:
    from app.config import Config
    from app.utils.helpers import ensure_data_dir
except ImportError:
    # Fallback for standalone testing
    def ensure_data_dir(path): os.makedirs(path, exist_ok=True)
    class Config: DEFAULT_SEARCH_PATHS = [os.environ.get('ProgramData', '')]

class Scanner:
    def __init__(self, db_path=os.path.join(Config.DATA_DIR, "file_index.db")):
        self.db_path = db_path
        # Ensure the directory exists before connecting
        os.makedirs(Path(db_path).parent, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Creates the table structure for tracking apps and frequency."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS file_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    path TEXT UNIQUE NOT NULL,
                    category TEXT, 
                    usage_count INTEGER DEFAULT 0,
                    last_accessed REAL,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            conn.commit()

    def scan_system(self):
        """
        Scans common directories to find installed applications.
        Adjust search_paths in config.py for your specific OS.
        """
        search_paths = getattr(Config, 'SCAN_PATHS', [])
        logger.info(f"Scanning system for programs in: {search_paths}")
        
        found_items = []
        for path_str in search_paths:
            root_path = Path(path_str)
            if not root_path.exists(): continue

            # Looking for common executable/shortcut types
            for ext in ['*.exe', '*.lnk']:
                for entry in root_path.rglob(ext):
                    try:
                        found_items.append((entry.stem, str(entry.absolute()), 'app'))
                    except (PermissionError, OSError):
                        continue

        self._update_index(found_items)
        logger.info(f"Index updated with {len(found_items)} items.")

    def _update_index(self, items):
        """Efficiently inserts new items while ignoring existing ones."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany("""
                INSERT OR IGNORE INTO file_index (name, path, category, last_accessed)
                VALUES (?, ?, ?, ?)
            """, [(item[0], item[1], item[2], time.time()) for item in items])
            conn.commit()

    def track_running_processes(self):
        """
        Scans currently running processes. 
        If a running process matches a known app in our DB, increment usage.
        """
        running_names = {p.info['name'].lower() for p in psutil.process_iter(['name'])}
        
        with sqlite3.connect(self.db_path) as conn:
            # We fetch apps where the name (lowercase) is in the running processes list
            cursor = conn.execute("SELECT id, name FROM file_index WHERE category = 'app'")
            apps = cursor.fetchall()
            
            for app_id, app_name in apps:
                # Check if 'chrome.exe' or similar is running
                if any(app_name.lower() in p_name for p_name in running_names):
                    conn.execute("""
                        UPDATE file_index 
                        SET usage_count = usage_count + 1, last_accessed = ? 
                        WHERE id = ?
                    """, (time.time(), app_id))
            conn.commit()
        logger.info("Usage frequency updated based on active processes.")

    def get_top_items(self, limit=5):
        """Returns the top apps based on usage count."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT name, path FROM file_index 
                ORDER BY usage_count DESC, last_accessed DESC 
                LIMIT ?
            """, (limit,))
            return [{'name': row[0], 'path': row[1]} for row in cursor.fetchall()]

    def index_all(self):
        """Public alias for scan_system"""
        self.scan_system()

    def update_access(self, path):
        """Update usage for accessed path"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE file_index 
                SET usage_count = usage_count + 1, last_accessed = ?
                WHERE path = ? OR name = ?
            """, (time.time(), path, os.path.basename(path) or path))
            conn.commit()
        logger.info(f"Updated access for {path}")

# Entry point for testing the scanner independently
if __name__ == "__main__":
    indexer = Scanner()
    indexer.index_all()
    indexer.track_running_processes()
    print("Your top apps:", indexer.get_top_items(5))
