import datetime
import os
import sys
import psutil

# Add parent directory to sys.path so database imports work smoothly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_write import save_computational
from database.db_read import get_latest_computational

def collect_computational() -> dict:
    """
    Captures live machine hardware metrics using psutil,
    saves the record to SQLite, and returns the dictionary.
    """
    # 1. Capture live system metrics
    # interval=1 measures CPU usage over 1 second for accurate reading
    cpu_percent = psutil.cpu_percent(interval=1)
    ram_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    process_count = len(psutil.pids())
    
    # 2. Format timestamp as required: YYYY-MM-DD HH:MM:SS
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 3. Pack into dictionary matching exact database column names
    data = {
        "timestamp": timestamp,
        "cpu_percent": float(cpu_percent),
        "ram_percent": float(ram_percent),
        "disk_percent": float(disk_percent),
        "running_processes": int(process_count)
    }

    # 4. Save to database
    save_computational(data)
    return data

def get_computational_summary(limit: int = 20) -> list[dict]:
    """Retrieves recent computational telemetry records from SQLite."""
    return get_latest_computational(limit=limit)

if __name__ == "__main__":
    print("Collecting live computational telemetry...")
    result = collect_computational()
    print("✅ Successfully collected and saved:", result)
