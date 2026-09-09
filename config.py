import os
from dotenv import load_dotenv

load_dotenv()

# Database File Name
DATABASE_PATH = "resourceiq.db"

# Groq AI Settings - Using confirmed active model from your key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "qwen/qwen3.8-27b"

# External API Endpoints
ARXIV_BASE_URL = "http://export.arxiv.org/api/query"
SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1"
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
