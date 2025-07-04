"""Essential health check tasks."""

import logging
from datetime import datetime, timezone
from ..celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, name="health_ping")
def health_ping(self):
    """Essential health ping task."""
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "worker_id": self.request.id,
            "message": "Worker is responsive"
        }
    except Exception as e:
        logger.error(f"Health ping failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": str(e)
        }
