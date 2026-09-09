from fastapi import APIRouter

router = APIRouter(prefix="/api/human", tags=["Human Resources"])

@router.get("/collect")
async def collect():
    return {"status": "placeholder — Member 5 will implement"}

@router.get("/summary")
async def summary():
    return []
