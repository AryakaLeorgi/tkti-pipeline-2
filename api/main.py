from fastapi import FastAPI
from routes import analyze, recommend, pipeline

app = FastAPI(
    title="AI DevOps Assistant API",
    version="1.0.0"
)

app.include_router(analyze.router, prefix="/analyze", tags=["Analyze Logs"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommendation"])
app.include_router(pipeline.router, prefix="/pipeline", tags=["CI/CD Pipeline"])
