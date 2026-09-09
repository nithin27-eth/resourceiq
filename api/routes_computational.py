from fastapi import APIRouter

router = APIRouter(prefix="/api/computational", tags=["Computational"])

@router.get("/collect")
async def collect():
    return {"status": "placeholder — Member 3 will implement"}

@router.get("/summary")
async def summary():
    return []
