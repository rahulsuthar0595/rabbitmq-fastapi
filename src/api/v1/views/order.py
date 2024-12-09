from fastapi import APIRouter

from src.api.v1.services.rabbit_mq.producer import RabbitMQProducer

router = APIRouter(prefix="/order")

@router.post("/make-order")
async def make_order():
    order_details = {
        "order_id": 12345,
        "customer_name": "John Doe",
        "items": [
            {"item": "Burger", "quantity": 2},
            {"item": "Fries", "quantity": 1}
        ],
        "total": 15.50
    }
    rabbitmq = RabbitMQProducer()
    await rabbitmq.publish(queue_name='order_queue', message=order_details)