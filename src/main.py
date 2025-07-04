"""Main FastAPI application entry point."""

from fastapi import FastAPI
from src.api.routes import health

app = FastAPI(
    title="Microservice Template",
    description="Auto-configurable microservice foundation",
    version="1.0.0"
)

# Include routers
app.include_router(health.router)

@app.get("/")
async def root():
    return {"message": "Microservice Template - Ready for customization"}
