import os
import random
import time
from datetime import datetime

from PIL import Image
from celery.exceptions import MaxRetriesExceededError

from logger.logger import logger
from workers.celery_config import celery

MEDIA_UPLOAD_DIR = "media"
os.makedirs(MEDIA_UPLOAD_DIR, exist_ok=True)


@celery.task()
def convert_image_to_png(image_path: str):
    try:
        time.sleep(10)
        img = Image.open(image_path)
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(MEDIA_UPLOAD_DIR, f"{base_name}.png")
        img.convert("RGBA").save(output_path, format="PNG")
        return {"message": "Image converted successfully", "output_path": output_path}
    except Exception as e:
        return {"error": str(e)}


@celery.task(bind=True, max_retries=3, default_retry_delay=10)
def send_reminder(self, message: str):
    msg = f"Sending Reminder: {message} at {datetime.now()}"
    try:
        if random.choice([True, False]):
            logger.info(msg)
            return {"message": msg}
        else:
            raise ValueError("Send reminder event failed")
    except Exception as exc:
        logger.error(f"Task failed: {exc}, retrying after some time....")
        try:
            self.retry(exc=exc)
        except MaxRetriesExceededError:
            logger.error(f"Max retries exceed for message - {message}")
            return {"message": "Task failed after max retries."}


@celery.task(name="cron_beat_every_min")
def cron_beat_task(message: str, **kwargs: dict):
    logger.info(f"Cron Beat task executed successfully with argument - {message} and kwargs - {kwargs}")
    return {"message": "Success"}
