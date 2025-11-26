from pydantic import BaseModel
from typing import Optional, List

class LogInput(BaseModel):
    pipeline_id: Optional[str] = None
    raw_log: str

class RCAResult(BaseModel):
    root_cause: str
    category: str
    confidence: float

class RecommendationResult(BaseModel):
    fix_description: str
    updated_code_snippet: Optional[str] = None
    severity: str

class PipelineInfo(BaseModel):
    pipeline_name: str
    status: str
    duration: Optional[float] = None
