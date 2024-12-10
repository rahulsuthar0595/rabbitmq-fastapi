import json

from logger.logger import logger
from src.api.v1.services.rabbit_mq.base import BaseRabbitMQ


class RabbitMQConsumer(BaseRabbitMQ):

    @staticmethod
    def common_callback(ch, method, properties, body):
        decoded_data = json.loads(body)
        logger.info(f"decoded_data: {decoded_data}")

    @staticmethod
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

    def consume(self, queue_name):
        if not self.channel:
            raise Exception("Connection is not established.")

        if queue_name == "order_queue":
            callback = self.process_order_callback
        else:
            callback = self.common_callback
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.start_consuming()
