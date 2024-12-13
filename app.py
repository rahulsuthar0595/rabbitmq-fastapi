import asyncio
import json
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.config import settings
from logger.logger import logger
from src.api.v1.services.kafka.kafka import kafka_consumer
from src.api.v1.services.rabbit_mq.consumer import RabbitMQConsumer
from src.api.v1.services.redis.redis_config import RedisBroker
from src.route.router import router


def process_order_callback(ch, method, properties, body):
    data = json.loads(body)
    order = data.get("message")
    # Simulate processing the order (e.g., preparing the food)
    logger.info(f"Processing order {order['order_id']} for {order['customer_name']}")
    logger.info(f"Processing order {order['order_id']} for {order['customer_name']}")
    logger.info("Items to prepare:")
    for item in order['items']:
        logger.info(f"- {item['quantity']} x {item['item']}")

    # Simulate order completion (e.g., delivery)
    logger.info(f"Order {order['order_id']} completed! Total: ${order['total']}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread1 = threading.Thread(target=RabbitMQConsumer().consume, args=("order_queue", process_order_callback))
    thread1.start()  # Keeps the thread running as long as FastAPI app is running
    thread2 = threading.Thread(target=RedisBroker().consume, args={settings.LEADERBOARD_REDIS_CHANNEL})
    thread2.start()  # Keeps the thread running as long as FastAPI app is running
    asyncio.create_task(kafka_consumer())
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
