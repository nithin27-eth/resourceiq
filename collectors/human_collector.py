import datetime
import json
import os
import sys
import requests

# Add root directory to sys.path so config and database layers can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import GITHUB_API_URL, GITHUB_TOKEN
from database.db_write import save_human
from database.db_read import get_latest_human

def get_github_headers() -> dict:
    """Constructs authorization headers for GitHub API."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

def collect_github_activity(repo_owner: str = "torvalds", repo_name: str = "linux") -> list[dict]:
    """
    Pulls live contributor statistics, open issues, and languages from GitHub API.
    Falls back to mock_data/human_mock.json if rate-limited or offline.
    """
    collected_records = []
    headers = get_github_headers()
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # 1. Fetch Contributors (Commit counts)
        contrib_url = f"{GITHUB_API_URL}/repos/{repo_owner}/{repo_name}/contributors?per_page=6"
        res_contrib = requests.get(contrib_url, headers=headers, timeout=10)

        # 2. Fetch Open Issues (Assignee distribution)
        issues_url = f"{GITHUB_API_URL}/repos/{repo_owner}/{repo_name}/issues?state=open&per_page=50"
        res_issues = requests.get(issues_url, headers=headers, timeout=10)

        # 3. Fetch Repo Languages
        lang_url = f"{GITHUB_API_URL}/repos/{repo_owner}/{repo_name}/languages"
        res_lang = requests.get(lang_url, headers=headers, timeout=10)

        if res_contrib.status_code == 200:
            contributors = res_contrib.json()
            
            # Map issues count to user logins
            issue_counts = {}
            if res_issues.status_code == 200:
                issues = res_issues.json()
                for issue in issues:
                    assignee = issue.get("assignee")
                    if assignee:
                        login = assignee.get("login")
                        issue_counts[login] = issue_counts.get(login, 0) + 1

            # Format top 3 languages
            languages_str = "General"
            if res_lang.status_code == 200:
                languages = list(res_lang.json().keys())[:3]
                languages_str = ", ".join(languages) if languages else "Code"

            for c in contributors[:6]:
                login = c.get("login", "unknown")
                commits = c.get("contributions", 0)
                open_issues = issue_counts.get(login, 0)

                record = {
                    "timestamp": current_time,
                    "member_name": login,
                    "repo_name": f"{repo_owner}/{repo_name}",
                    "commits_last_week": int(commits),
                    "open_issues_assigned": int(open_issues),
                    "languages_used": languages_str
                }
                save_human(record)
                collected_records.append(record)

            return collected_records

    except Exception as e:
        print(f"⚠️ Live GitHub API query encountered an error: {e}")

    # Fallback to high-contrast mock data if API call failed or rate-limited
    print("ℹ️ Loading high-contrast human mock data fallback for demo safety...")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    mock_path = os.path.join(base_dir, "mock_data", "human_mock.json")
    try:
        with open(mock_path, "r", encoding="utf-8") as f:
            mock_entries = json.load(f)
            for entry in mock_entries:
                entry["timestamp"] = current_time
                save_human(entry)
                collected_records.append(entry)
    except Exception as mock_err:
        print(f"❌ Failed to load human mock data: {mock_err}")

    return collected_records

def get_human_summary(limit: int = 20) -> list[dict]:
    """Retrieves stored human resource records from SQLite."""
    return get_latest_human(limit=limit)

if __name__ == "__main__":
    print("Testing Human Collector on GitHub...")
    results = collect_github_activity("fastapi", "fastapi")
    print(f"✅ Successfully collected and saved {len(results)} team records.")
