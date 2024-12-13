import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.config import settings
from src.api.v1.services.kafka.kafka import kafka_consumer
from src.route.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(kafka_consumer(settings.KAFKA_TOPIC_NAME, settings.KAFKA_GROUP_NAME))
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
