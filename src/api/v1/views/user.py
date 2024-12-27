import os
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from celery.result import AsyncResult
from fastapi import APIRouter, UploadFile, File

from workers.tasks import convert_image_to_png, send_reminder

router = APIRouter(prefix="/user")

MEDIA_UPLOAD_DIR = "media"
os.makedirs(MEDIA_UPLOAD_DIR, exist_ok=True)


@router.post("/upload-picture/")
async def upload_profile_picture(file: UploadFile = File()):
    file_name = f"{uuid4().hex}_{file.filename}"
    file_path = os.path.join(MEDIA_UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    task = convert_image_to_png.apply_async(args=[file_path])
    return {"message": "Image processing in background", "task_id": task.id}


@router.get("/task_status/{task_id}")
async def get_task_status(task_id: str):
    task = AsyncResult(task_id)
    task_result_mapper = {
        "PENDING": {"task_id": task_id, "status": "Task is still in progress"},
        "SUCCESS": {"task_id": task_id, "status": "Task completed", "result": task.result},
        "FAILURE": {"task_id": task_id, "status": "Task failed", "error": str(task.info)}
    }
    return task_result_mapper.get(task.state, {"task_id": task_id, "status": task.state})


@router.post("/schedule_reminder/")
async def schedule_reminder(message: str, eta_seconds: int):
    eta_datetime = datetime.now(timezone.utc) + timedelta(seconds=eta_seconds)
    # Execute task at the eta (Estimated Time of Arrival).
    task = send_reminder.apply_async(args=[message], eta=eta_datetime)
    return {"message": "Reminder task scheduled", "task_id": task.id}
