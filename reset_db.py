"""
Reset script for Zenith '26 Fest System.
Clears all student registrations and resets available seats to full capacity.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "fest.db"

def reset_registrations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM registrations;")
    conn.commit()
    count = cursor.execute("SELECT COUNT(*) FROM registrations;").fetchone()[0]
    conn.close()
    print(f"Database reset complete! Active registrations: {count}. All event seats are now 100% available.")

if __name__ == "__main__":
    reset_registrations()
