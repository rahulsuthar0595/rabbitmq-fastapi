from fastapi import APIRouter

from config.config import settings
from src.api.v1.services.kafka.kafka import kafka_producer

router = APIRouter(prefix="/order")


@router.post("/send-message")
async def send_message(email: str, message: str):
    data = {"email": email, "message": message}
    await kafka_producer(settings.KAFKA_TOPIC_NAME, data)
    return {"message": "Success"}
