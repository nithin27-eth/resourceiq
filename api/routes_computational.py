from fastapi import APIRouter
from collectors.computational_collector import collect_computational, get_computational_summary

router = APIRouter(prefix="/api/computational", tags=["Computational"])

@router.get("/collect")
async def collect_endpoint():
    """Triggers live system hardware telemetry collection and stores in DB."""
    data = collect_computational()
    return {
        "status": "success",
        "message": "Telemetry collected and saved to SQLite",
        "data": data
    }

@router.get("/summary")
async def summary_endpoint(limit: int = 20):
    """Returns the latest computational telemetry records as JSON."""
    records = get_computational_summary(limit=limit)
    return records
