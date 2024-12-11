import json

import pika

from logger.logger import logger
from src.api.v1.services.rabbit_mq.base import BaseRabbitMQ


class RabbitMQProducer(BaseRabbitMQ):

    async def publish(self, queue_name, message):
        try:
            if not self.channel:
                raise Exception("Connection is not established.")
            body = json.dumps({"message": message})
            self.channel.queue_declare(queue_name, durable=True)
            # delivery_mode 1 (Non-Persistent):
            # The message is stored only in memory. If RabbitMQ crashes or restarts, the message will be lost.
            # delivery_mode 2 (Persistent):
            # The message is stored on disk. If RabbitMQ crashes or restarts, the message can be recovered.
            # durable ensures that the queue survives a RabbitMQ crash or restart and recreated after a broker restart.
            # delivery_mode makes the message persistent/non-persistent.
            self.channel.basic_publish(
                exchange="", routing_key=queue_name, body=body,
                properties=pika.BasicProperties(delivery_mode=2)
            )
            logger.info(f"Sent message to queue {queue_name}: {message}")
        except Exception as e:
            logger.error(f"Exception in Rabbit MQ Publish: {str(e)}")
            raise e
        finally:
            self.close_connection()
