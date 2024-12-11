from src.api.v1.services.rabbit_mq.base import BaseRabbitMQ


class RabbitMQConsumer(BaseRabbitMQ):
    def consume(self, queue_name, callback):
        if not self.channel:
            raise Exception("Connection is not established.")

        self.channel.queue_declare(queue_name, durable=True)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.start_consuming()
