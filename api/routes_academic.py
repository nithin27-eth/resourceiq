from fastapi import APIRouter, Query
from collectors.academic_collector import collect_academic, get_academic_summary

router = APIRouter(prefix="/api/academic", tags=["Academic"])

@router.get("/collect")
async def collect_endpoint(topic: str = Query("resource optimization AI", description="Research topic to search")):
    """Searches arXiv & Semantic Scholar, saves results to SQLite."""
    papers = collect_academic(topic=topic)
    return {
        "status": "success",
        "topic": topic,
        "count": len(papers),
        "data": papers
    }

@router.get("/summary")
async def summary_endpoint(limit: int = 20):
    """Returns stored research papers as JSON."""
    return get_academic_summary(limit=limit)
