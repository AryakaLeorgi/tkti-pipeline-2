from fastapi import APIRouter
from models.schemas import LogInput, RCAResult
from services.rca_engine import RCAEngine

router = APIRouter()
rca_engine = RCAEngine()

@router.post("/log", response_model=RCAResult)
def analyze_log(data: LogInput):
    return rca_engine.analyze(data.raw_log)
