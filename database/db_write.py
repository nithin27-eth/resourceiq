import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_setup import get_connection

def save_computational(data: dict):
    """
    Saves a single computational record.
    Expected keys: timestamp, cpu_percent, ram_percent, disk_percent, running_processes
    """
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO computational_data 
        (timestamp, cpu_percent, ram_percent, disk_percent, running_processes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["timestamp"],
            data["cpu_percent"],
            data["ram_percent"],
            data["disk_percent"],
            data["running_processes"],
        ),
    )
    conn.commit()
    conn.close()

def save_energy(data: dict):
    """
    Saves a single energy record.
    Expected keys: timestamp, building_name, kwh_consumed, device_count, peak_hours
    """
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO energy_data 
        (timestamp, building_name, kwh_consumed, device_count, peak_hours)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["timestamp"],
            data["building_name"],
            data["kwh_consumed"],
            data["device_count"],
            data["peak_hours"],
        ),
    )
    conn.commit()
    conn.close()

def save_human(data: dict):
    """
    Saves a single human resource record.
    Expected keys: timestamp, member_name, repo_name, commits_last_week, 
                   open_issues_assigned, languages_used
    """
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO human_data 
        (timestamp, member_name, repo_name, commits_last_week, 
         open_issues_assigned, languages_used)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data["timestamp"],
            data["member_name"],
            data["repo_name"],
            data["commits_last_week"],
            data["open_issues_assigned"],
            data["languages_used"],
        ),
    )
    conn.commit()
    conn.close()

def save_academic(data: dict):
    """
    Saves a single research paper record.
    Expected keys: timestamp, query_topic, paper_title, authors, year, 
                   abstract, citation_count, source
    """
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO academic_data 
        (timestamp, query_topic, paper_title, authors, year, 
         abstract, citation_count, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["timestamp"],
            data["query_topic"],
            data["paper_title"],
            data["authors"],
            data["year"],
            data["abstract"],
            data["citation_count"],
            data["source"],
        ),
    )
    conn.commit()
    conn.close()
