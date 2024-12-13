import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.config import settings
from src.api.v1.services.redis.redis_config import RedisBroker
from src.route.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=RedisBroker().consume, args={settings.LEADERBOARD_REDIS_CHANNEL})
    thread.start()  # Keeps the thread running as long as FastAPI app is running
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
