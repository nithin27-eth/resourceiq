import sqlite3
import sys
import os

# Add the project root directory to sys.path so config can always be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DATABASE_PATH

def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    row_factory = sqlite3.Row allows accessing columns by name like a dictionary.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """
    Creates the 4 domain tables if they do not exist yet.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 1. COMPUTATIONAL TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS computational_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            cpu_percent REAL,
            ram_percent REAL,
            disk_percent REAL,
            running_processes INTEGER
        )
    """)

    # 2. ENERGY TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS energy_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            building_name TEXT,
            kwh_consumed REAL,
            device_count INTEGER,
            peak_hours TEXT
        )
    """)

    # 3. HUMAN RESOURCES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS human_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            member_name TEXT,
            repo_name TEXT,
            commits_last_week INTEGER,
            open_issues_assigned INTEGER,
            languages_used TEXT
        )
    """)

    # 4. ACADEMIC TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS academic_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            query_topic TEXT,
            paper_title TEXT,
            authors TEXT,
            year INTEGER,
            abstract TEXT,
            citation_count INTEGER,
            source TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ All 4 database tables created/verified successfully.")

if __name__ == "__main__":
    initialize_database()
