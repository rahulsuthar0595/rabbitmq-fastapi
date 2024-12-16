import json

import pika

from config.config import settings
from logger.logger import logger


class RabbitMQBroker:
    def __init__(self):
        self.host = settings.RABBITMQ_HOST
        self.port = settings.RABBITMQ_PORT
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        parameters = pika.ConnectionParameters(host=self.host, port=self.port)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def close_connection(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def consume(self, queue_name, callback):
        if not self.channel:
            raise Exception("Connection is not established.")

        self.channel.queue_declare(queue_name, durable=True)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.start_consuming()

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
