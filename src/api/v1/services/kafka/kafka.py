import json

import aiokafka

from config.config import settings
from logger.logger import logger


async def kafka_consumer(topic: str, group_id: str):
    while True:
        consumer = None
        try:
            consumer = aiokafka.AIOKafkaConsumer(
                topic,
                bootstrap_servers=settings.KAFKA_SERVER_URL,
                group_id=group_id,
                enable_auto_commit=True,
                # If set to False, then have to use consumer.commit() method to manually commit.
                auto_commit_interval_ms=1000,  # Autocommit every second
                auto_offset_reset="earliest",
            )
            await consumer.start()

            logger.info(f"Kafka Consumer: Started")

            async for message in consumer:
                logger.info(f"Kafka Consumer: Key: {message.key} - Value: {message.value}")
                # await consumer.commit()   # If enable_auto_commit=False, then use this.
        except Exception as e:
            logger.error(f"Exception: Kafka Consumer: {str(e)}")
        finally:
            await consumer.stop()


async def kafka_producer(topic: str, data: dict):
    producer = aiokafka.AIOKafkaProducer(bootstrap_servers=settings.KAFKA_SERVER_URL)
    await producer.start()
    try:
        data = json.dumps({"data": data})
        logger.info(f"Kafka Producer: data : {data}")
        await producer.send_and_wait(topic, data.encode("utf-8"))
    except Exception as e:
        logger.error(f"Exception: Kafka Producer: {str(e)}")
    finally:
        await producer.stop()
