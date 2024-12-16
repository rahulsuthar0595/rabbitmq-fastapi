import threading
import json
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.config import settings
from src.api.v1.services.redis.redis_config import RedisBroker
from logger.logger import logger
from src.api.v1.services.rabbit_mq.rabbit_mq_config import RabbitMQBroker
from src.api.v1.services.kafka.kafka import kafka_consumer
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
    thread = threading.Thread(target=RedisBroker().consume, args={settings.LEADERBOARD_REDIS_CHANNEL})
    thread.start()  # Keeps the thread running as long as FastAPI app is running
    thread = threading.Thread(target=RabbitMQBroker().consume, args=(settings.RABBIT_MQ_ORDER_QUEUE, process_order_callback))
    thread.start()  # Keeps the thread running as long as FastAPI app is running
    asyncio.create_task(kafka_consumer(settings.KAFKA_TOPIC_NAME, settings.KAFKA_GROUP_NAME))
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
