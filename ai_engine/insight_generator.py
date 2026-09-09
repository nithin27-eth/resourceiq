import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_read import (
    get_latest_computational,
    get_latest_energy,
    get_latest_human,
    get_latest_academic,
)
from ai_engine.prompt_builder import build_prompt
from ai_engine.groq_client import ask_groq

DOMAIN_READERS = {
    "computational": get_latest_computational,
    "energy": get_latest_energy,
    "human": get_latest_human,
    "academic": get_latest_academic,
}

def generate_insight(domain: str, user_question: str) -> str:
    """
    Main orchestrator:
    1. Reads latest domain data from SQLite
    2. Builds structured prompt
    3. Sends to Groq AI
    4. Returns recommendation
    """
    clean_domain = domain.lower().strip()

    if clean_domain not in DOMAIN_READERS:
        return f"❌ Invalid domain '{domain}'. Supported domains: {list(DOMAIN_READERS.keys())}"

    reader_func = DOMAIN_READERS[clean_domain]
    data_records = reader_func(limit=20)

    prompt = build_prompt(clean_domain, data_records, user_question)
    insight = ask_groq(prompt)
    return insight

if __name__ == "__main__":
    print("Testing generate_insight on computational domain...")
    test_insight = generate_insight(
        domain="computational",
        user_question="Is the system experiencing high load, and what should we do?"
    )
    print("\n--- AI INSIGHT RESULT ---")
    print(test_insight)
