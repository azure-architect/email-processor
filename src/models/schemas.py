"""Essential data models."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any, Dict

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    message: Optional[str] = None

class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    data: Optional[Dict[str, Any]] = None
