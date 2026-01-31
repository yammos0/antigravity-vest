from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "antigravity_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Defined queues for priority
    task_queues={
        "high_priority": {"exchange": "high_priority", "routing_key": "high"},
        "default": {"exchange": "default", "routing_key": "default"},
    },
    task_default_queue="default",
    task_default_exchange="default",
    task_default_routing_key="default",
)

# Auto-discover tasks in packages
celery_app.autodiscover_tasks(["app.tasks"])
