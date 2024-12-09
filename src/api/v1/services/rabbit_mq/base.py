import pika

from config.config import settings


class BaseRabbitMQ:
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

