"""Essential health check endpoints."""

from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "microservice-template"
    }
