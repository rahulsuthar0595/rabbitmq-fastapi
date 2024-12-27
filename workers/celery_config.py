from celery import Celery
from celery.schedules import crontab

from config.config import settings

celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)
celery.autodiscover_tasks(["workers"], force=True)

celery.conf.beat_schedule = {
    "every-min-cron-beat": {
        "task": "cron_beat_every_min",
        "schedule": crontab(minute="*/1"),
        "args": ("This is sample test message.",),
        "kwargs": {"extra_key": "info"}
    }
}
