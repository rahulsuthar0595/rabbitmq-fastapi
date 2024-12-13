from fastapi import APIRouter

from config.config import settings
from src.api.v1.services.rabbit_mq.rabbit_mq_config import RabbitMQBroker

router = APIRouter(prefix="/order")


@router.post("/create-order")
async def create_order():
    order_details = {
        "order_id": 12345,
        "customer_name": "John Doe",
        "items": [
            {"item": "Burger", "quantity": 2},
            {"item": "Fries", "quantity": 1}
        ],
        "total": 15.50
    }
    rabbitmq = RabbitMQBroker()
    await rabbitmq.publish(queue_name=settings.RABBIT_MQ_ORDER_QUEUE, message=order_details)
    return {"message": "Success"}
