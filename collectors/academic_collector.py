import datetime
import json
import os
import sys
import xml.etree.ElementTree as ET
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_write import save_academic
from database.db_read import get_latest_academic
from config import ARXIV_BASE_URL, SEMANTIC_SCHOLAR_URL

def fetch_arxiv_papers(topic: str, max_results: int = 5) -> list[dict]:
    """Queries arXiv API (XML) for academic papers on the specified topic."""
    papers = []
    try:
        url = f"{ARXIV_BASE_URL}?search_query=all:{requests.utils.quote(topic)}&start=0&max_results={max_results}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            # Namespace used by arXiv Atom feed
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                published = entry.find('atom:published', ns).text[:4] # Extract Year
                
                # Extract author names
                authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
                authors_str = ", ".join(authors[:3])
                if len(authors) > 3:
                    authors_str += " et al."
                
                papers.append({
                    "timestamp": timestamp,
                    "query_topic": topic,
                    "paper_title": title,
                    "authors": authors_str,
                    "year": int(published) if published.isdigit() else 2024,
                    "abstract": summary[:300] + "...",
                    "citation_count": 0,
                    "source": "arXiv"
                })
    except Exception as e:
        print(f"⚠️ arXiv API error: {e}")
        
    return papers

def fetch_semantic_scholar_papers(topic: str, limit: int = 5) -> list[dict]:
    """Queries Semantic Scholar API (JSON) for academic papers and citation counts."""
    papers = []
    try:
        url = f"{SEMANTIC_SCHOLAR_URL}/paper/search"
        params = {
            "query": topic,
            "limit": limit,
            "fields": "title,authors,year,citationCount,abstract"
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            for item in data.get("data", []):
                title = item.get("title", "Untitled")
                year = item.get("year") or 2024
                citation_count = item.get("citationCount") or 0
                abstract = item.get("abstract") or "No abstract available."
                
                author_names = [a.get("name", "") for a in item.get("authors", [])]
                authors_str = ", ".join(author_names[:3])
                if len(author_names) > 3:
                    authors_str += " et al."
                
                papers.append({
                    "timestamp": timestamp,
                    "query_topic": topic,
                    "paper_title": title,
                    "authors": authors_str if authors_str else "Unknown",
                    "year": int(year),
                    "abstract": abstract[:300] + "...",
                    "citation_count": int(citation_count),
                    "source": "Semantic Scholar"
                })
    except Exception as e:
        print(f"⚠️ Semantic Scholar API error: {e}")
        
    return papers

def collect_academic(topic: str = "resource allocation cloud computing") -> list[dict]:
    """
    Collects papers from both arXiv and Semantic Scholar,
    saves each to SQLite, and falls back to mock_data if offline.
    """
    combined_papers = []
    
    # 1. Fetch live papers from arXiv
    arxiv_results = fetch_arxiv_papers(topic, max_results=4)
    combined_papers.extend(arxiv_results)
    
    # 2. Fetch live papers from Semantic Scholar
    ss_results = fetch_semantic_scholar_papers(topic, limit=4)
    combined_papers.extend(ss_results)
    
    # 3. Fallback to mock data if all API calls failed
    if not combined_papers:
        print("ℹ️ External APIs unreachable, loading academic mock data fallback...")
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        mock_path = os.path.join(base_dir, "mock_data", "academic_mock.json")
        try:
            with open(mock_path, "r", encoding="utf-8") as f:
                combined_papers = json.load(f)
        except Exception:
            pass
            
    # 4. Save to SQLite database
    for paper in combined_papers:
        save_academic(paper)
        
    return combined_papers

def get_academic_summary(limit: int = 20) -> list[dict]:
    """Retrieves stored research paper records from SQLite."""
    return get_latest_academic(limit=limit)

if __name__ == "__main__":
    print("Testing Academic Collector on 'Resource Intelligence'...")
    results = collect_academic(topic="resource intelligence machine learning")
    print(f"✅ Successfully collected and saved {len(results)} research papers.")
