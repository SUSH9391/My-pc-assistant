import sqlite3
import os
from pathlib import Path
from app.config import Config
from app.utils.helpers import ensure_data_dir

class FileIndexer:
    def __init__(self, db_path="data/file_index.db"):
        self.db_path = os.path.join(Config.BASE_DIR, db_path)
        ensure_data_dir()
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY,
                path TEXT UNIQUE,
                name TEXT,
                ext TEXT,
                size INTEGER,
                mtime REAL
            )
        """)
        conn.commit()
        conn.close()

    def index_directory(self, directory):
        conn = sqlite3.connect(self.db_path)
        for root, dirs, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, Config.BASE_DIR)
                stat = os.stat(path)
                conn.execute("""
                    INSERT OR REPLACE INTO files 
                    (path, name, ext, size, mtime) 
                    VALUES (?, ?, ?, ?, ?)
                """, (rel_path, file, Path(file).suffix, stat.st_size, stat.st_mtime))
        conn.commit()
        conn.close()
        print(f"Indexed {directory}")
