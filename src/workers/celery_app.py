"""Essential Celery application configuration."""

from celery import Celery
from celery.schedules import crontab
import os

# Create Celery app
celery_app = Celery(
    "microservice-template",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    include=[
        "src.workers.tasks.health_tasks",
        "src.workers.tasks.email_tasks",
        "src.workers.tasks.attachment_processing_tasks",
    ],
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    result_expires=3600,
    beat_schedule={
        "five-minute-timer": {
            "task": "src.workers.tasks.health_tasks.five_minute_timer",
            "schedule": 300.0,  # 5 minutes = 300 seconds
        },
    },
)
