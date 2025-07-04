"""
Example task template - replace with your business logic.

TODO: This is a template file. Copy to src/workers/tasks/ and customize.
"""

from datetime import datetime
from src.workers.celery_app import celery_app

@celery_app.task(bind=True, name="example_business_task")
def example_business_task(self, data):
    """
    Example task - replace with your implementation.
    
    TODO: Add your business logic here.
    """
    try:
        # TODO: Replace with your actual task logic
        result = {
            "input_data": data,
            "processed_at": datetime.utcnow().isoformat(),
            "status": "completed",
            "message": "TODO: Replace with your business logic"
        }
        return result
    except Exception as e:
        self.retry(countdown=60, max_retries=3)
