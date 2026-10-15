import sqlite3
import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# On Vercel / serverless platforms, only /tmp is writable
if os.environ.get("VERCEL"):
    DB_PATH = Path("/tmp") / "fest.db"
    ORIGINAL_DB = BASE_DIR / "fest.db"
    if not DB_PATH.exists() and ORIGINAL_DB.exists():
        try:
            shutil.copy2(ORIGINAL_DB, DB_PATH)
        except Exception as e:
            print(f"Error copying fest.db to /tmp: {e}")
else:
    DB_PATH = BASE_DIR / "fest.db"

def get_db_connection() -> sqlite3.Connection:
    """Returns a SQLite connection with Row factory enabled for column name access."""
    if os.environ.get("VERCEL"):
        if not DB_PATH.exists():
            ORIGINAL_DB = BASE_DIR / "fest.db"
            if ORIGINAL_DB.exists():
                try:
                    shutil.copy2(ORIGINAL_DB, DB_PATH)
                except Exception:
                    pass
            else:
                init_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Creates the events and registrations tables if they do not exist."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        event_date TEXT NOT NULL,
        event_time TEXT NOT NULL,
        venue TEXT NOT NULL,
        capacity INTEGER NOT NULL,
        fee INTEGER NOT NULL DEFAULT 0,
        icon TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER NOT NULL REFERENCES events(id),
        student_name TEXT NOT NULL,
        roll_number TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        registered_at TEXT NOT NULL,
        UNIQUE(event_id, email)
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized successfully at: {DB_PATH}")
