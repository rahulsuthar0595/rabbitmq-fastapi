from datetime import datetime, timedelta, timezone

from celery.result import AsyncResult
from fastapi import APIRouter

from workers.tasks import generate_user_invoice, acknowledge_task, schedule_after_api_call

router = APIRouter(prefix="/order")


@router.post("/generate-invoice")
async def generate_invoice(size: int):
    task = generate_user_invoice.delay(size)
    ack_task = acknowledge_task.delay(size)
    return {"message": "Success", "task_id": task.id, "ack_task_id": ack_task.id}


@router.get("/task-status")
async def check_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return result


@router.post("/schedule-one-time-task")
async def schedule_one_time_task(message: str):
    after_one_min = datetime.now(timezone.utc) + timedelta(seconds=10)  # ETA Time must be in UTC
    task = schedule_after_api_call.apply_async(args=[message], eta=after_one_min)
    return {"message": "Success", "task_id": task.id}
