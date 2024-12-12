from celery import Celery

from config.config import settings

celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)
celery.autodiscover_tasks(["workers"], force=True)

celery.conf.beat_schedule = {
    "5-sec-task": {
        "task": "five_sec_interval_task",
        "schedule": 5.0,  # Time in seconds. We can also use crontab() and schedule()
        "args": (),
    }
}