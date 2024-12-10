from celery import Celery

from config.config import settings

celery = Celery(
    "workers",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)
celery.autodiscover_tasks([
    "workers.tasks"
], force=True)

celery.conf.beat_schedule = {
    "5-sec-task": {
        "task": "five_sec_interval_task",
        "schedule": 5.0,  # Instead of time in seconds, can be used crontab and schedule
        "args": (),
    }
}