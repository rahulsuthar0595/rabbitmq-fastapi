import time

from celery import shared_task

from logger.logger import logger
from workers.worker import celery


@celery.task
def generate_user_invoice(size: int):
    time.sleep(size * 10)
    if size % 2 == 0:
        return True
    return False


@shared_task
def acknowledge_task(size: int):
    time.sleep(size * 10)
    return {"message": "Acknowledged task."}


@celery.task(name="five_sec_interval_task")
def five_sec_interval_task():
    logger.info("five_sec_interval_task executed.")
    return True


@celery.task(bind=True, max_retries=3)
def schedule_after_api_call(self, message: str):
    try:
        if getattr(self, "is_raise_validation", True):
            raise Exception("Something went wrong.")

        logger.info(f"schedule_after_api_call {message}")
        return True
    except Exception as exc:
        logger.error(f"schedule_after_api_call error: {exc}")
        # Retry the task if an exception occurs
        setattr(self, "is_raise_validation", False)
        raise self.retry(exc=exc, countdown=10)
