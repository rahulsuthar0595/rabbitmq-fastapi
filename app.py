import asyncio
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.services.kafka.kafka import kafka_consumer
from src.api.v1.services.rabbit_mq.consumer import RabbitMQConsumer
from src.api.v1.services.redis.redis_config import RedisBroker
from src.route.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread1 = threading.Thread(target=RabbitMQConsumer().consume, kwargs={"queue_name": "order_queue"})
    thread1.start()  # Keeps the thread running as long as FastAPI app is running
    thread2 = threading.Thread(target=RedisBroker(channel="leaderboard").consume)
    thread2.start()  # Keeps the thread running as long as FastAPI app is running
    asyncio.create_task(kafka_consumer())
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
