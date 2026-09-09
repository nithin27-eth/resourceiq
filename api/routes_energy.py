from fastapi import APIRouter

router = APIRouter(prefix="/api/energy", tags=["Energy"])

@router.get("/collect")
async def collect():
    return {"status": "placeholder — Member 4 will implement"}

@router.get("/summary")
async def summary():
    return []
