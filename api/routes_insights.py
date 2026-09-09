from fastapi import APIRouter
from pydantic import BaseModel, Field
from ai_engine.insight_generator import generate_insight

router = APIRouter(prefix="/api/insights", tags=["AI Insights"])

class InsightRequest(BaseModel):
    domain: str = Field(..., example="computational", description="Domain: computational, energy, human, academic")
    question: str = Field(..., example="Is my CPU usage dangerously high?", description="Question to ask AI")

@router.post("")
async def get_insight_endpoint(req: InsightRequest):
    """
    Accepts domain + question, pulls data from SQLite, returns Groq AI insight.
    """
    insight_text = generate_insight(domain=req.domain, user_question=req.question)
    return {
        "status": "success",
        "domain": req.domain,
        "question": req.question,
        "insight": insight_text
    }
