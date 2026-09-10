from fastapi import APIRouter, Query
from collectors.human_collector import collect_github_activity, get_human_summary

router = APIRouter(prefix="/api/human", tags=["Human Resources"])

@router.get("/collect")
async def collect_endpoint(
    owner: str = Query("fastapi", description="GitHub Repository Owner/Organization"),
    repo: str = Query("fastapi", description="GitHub Repository Name")
):
    """Fetches contributor workload & issues from GitHub, saves to SQLite."""
    records = collect_github_activity(repo_owner=owner, repo_name=repo)
    return {
        "status": "success",
        "repository": f"{owner}/{repo}",
        "count": len(records),
        "data": records
    }

@router.get("/summary")
async def summary_endpoint(limit: int = 20):
    """Returns stored human resource records as JSON."""
    return get_human_summary(limit=limit)
