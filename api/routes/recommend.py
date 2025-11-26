from fastapi import APIRouter
from models.schemas import LogInput, RecommendationResult
from services.fix_generator import FixGenerator

router = APIRouter()
fix_engine = FixGenerator()

@router.post("/fix", response_model=RecommendationResult)
def recommend_fix(data: LogInput):
    return fix_engine.generate_fix(data.raw_log)
