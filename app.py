import asyncio
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.services.kafka.kafka import kafka_consumer
from src.api.v1.services.rabbit_mq.consumer import RabbitMQConsumer
from src.route.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=RabbitMQConsumer().consume, kwargs={"queue_name": "order_queue"})
    thread.start()  # Keeps the thread running as long as FastAPI app is running
    asyncio.create_task(kafka_consumer())
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
