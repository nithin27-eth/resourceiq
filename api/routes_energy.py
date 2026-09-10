from fastapi import APIRouter
from collectors.energy_collector import collect_energy, get_energy_summary

router = APIRouter(prefix="/api/energy", tags=["Energy"])

@router.get("/collect")
async def collect_endpoint():
    """Triggers energy consumption data collection and saves to SQLite."""
    records = collect_energy()
    return {
        "status": "success",
        "message": f"Successfully collected {len(records)} energy records",
        "data": records
    }

@router.get("/summary")
async def summary_endpoint(limit: int = 20):
    """Returns the latest energy telemetry records as JSON."""
    return get_energy_summary(limit=limit)
