from fastapi import APIRouter
from models.schemas import PipelineInfo

router = APIRouter()

@router.get("/status", response_model=PipelineInfo)
def get_pipeline_status():
    return PipelineInfo(
        pipeline_name="sample-pipeline",
        status="running",
        duration=145.4
    )
