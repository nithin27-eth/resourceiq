import json
import os
import sys
import datetime

# Add root directory to sys.path for database imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_write import save_energy
from database.db_read import get_latest_energy

def collect_energy() -> list[dict]:
    """
    Collects energy consumption telemetry across buildings.
    Reads from mock_data/energy_mock.json, stamps current timestamp,
    saves records into SQLite, and returns the records.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    mock_file_path = os.path.join(base_dir, "mock_data", "energy_mock.json")
    
    collected_records = []
    
    try:
        with open(mock_file_path, "r", encoding="utf-8") as f:
            mock_entries = json.load(f)
            
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for entry in mock_entries:
            record = {
                "timestamp": current_time,
                "building_name": entry.get("building_name", "Main Building"),
                "kwh_consumed": float(entry.get("kwh_consumed", 0.0)),
                "device_count": int(entry.get("device_count", 0)),
                "peak_hours": entry.get("peak_hours", "N/A")
            }
            save_energy(record)
            collected_records.append(record)
            
        return collected_records
        
    except Exception as e:
        print(f"⚠️ Error collecting energy data: {e}")
        return []

def get_energy_summary(limit: int = 20) -> list[dict]:
    """Retrieves recent energy consumption records from SQLite."""
    return get_latest_energy(limit=limit)

if __name__ == "__main__":
    print("Testing Energy Collector...")
    records = collect_energy()
    print(f"✅ Successfully collected and saved {len(records)} energy records.")
