import json

import redis

from config.config import settings
from logger.logger import logger


class RedisBroker:
    def __init__(self, channel: str):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True
        )
        self.channel = channel

    def publish(self, data: dict):
        message = json.dumps(data)
        # Publish the message to the channel
        self.redis_client.publish(self.channel, message)

    def consume(self):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(self.channel)
        for message in pubsub.listen():
            logger.info(f"Consume message: {message}")
            if message and message["type"] == "message":
                logger.info(f"Received Redis Message From Consumer: {message['data']}")
