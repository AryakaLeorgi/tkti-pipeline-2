#!/usr/bin/env python3
"""
FastAPI server for ML Error Classification.
Provides /classify endpoint for error log classification.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

from model import get_classifier

app = FastAPI(
    title="ML Error Classifier",
    description="Classify CI/CD build errors using Machine Learning",
    version="1.0.0"
)

class ClassifyRequest(BaseModel):
    """Request body for /classify endpoint."""
    logs: str
    
class ClassifyResponse(BaseModel):
    """Response from /classify endpoint."""
    category: str
    fixable: bool
    priority: str
    confidence: float
    should_call_llm: bool
    reason: str

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    classifier = get_classifier()
    return {
        "status": "ok",
        "models_loaded": classifier.is_trained()
    }

@app.post("/classify", response_model=ClassifyResponse)
async def classify_error(request: ClassifyRequest):
    """
    Classify an error log.
    
    Returns classification results and recommendation on whether to call LLM.
    """
    classifier = get_classifier()
    
    if not classifier.is_trained():
        raise HTTPException(
            status_code=503,
            detail="Models not trained. Run train.py first."
        )
    
    # Get prediction
    result = classifier.predict(request.logs)
    
    # Determine if we should call LLM
    should_call_llm = result["fixable"] and result["confidence"] >= 0.5
    
    if not result["fixable"]:
        reason = f"Error type '{result['category']}' is not auto-fixable"
    elif result["confidence"] < 0.5:
        reason = f"Low confidence ({result['confidence']:.1%}), skipping LLM"
    else:
        reason = f"Error is fixable with {result['confidence']:.1%} confidence"
    
    return ClassifyResponse(
        category=result["category"],
        fixable=result["fixable"],
        priority=result["priority"],
        confidence=result["confidence"],
        should_call_llm=should_call_llm,
        reason=reason
    )

@app.get("/categories")
async def list_categories():
    """List all error categories."""
    return {
        "categories": [
            {"name": "syntax_error", "fixable": True, "description": "Code syntax issues"},
            {"name": "runtime_error", "fixable": True, "description": "Runtime type errors"},
            {"name": "test_failure", "fixable": True, "description": "Test assertion failures"},
            {"name": "dependency_error", "fixable": False, "description": "Package/module issues"},
            {"name": "config_error", "fixable": False, "description": "Configuration problems"},
            {"name": "network_error", "fixable": False, "description": "Network/connection issues"},
        ]
    }

if __name__ == "__main__":
    print("🚀 Starting ML Error Classifier Server...")
    uvicorn.run(app, host="0.0.0.0", port=3001)
