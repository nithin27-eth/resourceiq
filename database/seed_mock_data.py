import json
import os
import sys

# Ensure root directory is accessible for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_write import (
    save_computational,
    save_energy,
    save_human,
    save_academic,
)

def load_json_file(relative_path: str) -> list[dict]:
    """Reads a JSON file from disk and returns it as a list of Python dictionaries."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    full_path = os.path.join(base_dir, relative_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def seed_all():
    """Populates the database with all 4 mock datasets."""
    print("🌱 Seeding SQLite database with mock data...")

    # 1. Seed Computational
    comp_records = load_json_file("mock_data/computational_mock.json")
    for r in comp_records:
        save_computational(r)
    print(f"✅ Inserted {len(comp_records)} computational records.")

    # 2. Seed Energy
    energy_records = load_json_file("mock_data/energy_mock.json")
    for r in energy_records:
        save_energy(r)
    print(f"✅ Inserted {len(energy_records)} energy records.")

    # 3. Seed Human Resources
    human_records = load_json_file("mock_data/human_mock.json")
    for r in human_records:
        save_human(r)
    print(f"✅ Inserted {len(human_records)} human resource records.")

    # 4. Seed Academic
    academic_records = load_json_file("mock_data/academic_mock.json")
    for r in academic_records:
        save_academic(r)
    print(f"✅ Inserted {len(academic_records)} academic records.")

    print("\n🎉 Database successfully seeded with rich test data!")

if __name__ == "__main__":
    seed_all()
