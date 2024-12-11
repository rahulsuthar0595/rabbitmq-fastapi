import json

import aiokafka

from logger.logger import logger


async def kafka_consumer():
    while True:
        consumer = None
        try:
            consumer = aiokafka.AIOKafkaConsumer(
                "send_notification",
                bootstrap_servers="localhost:9092",
                group_id="notif_group",
                enable_auto_commit=True,  # If set to False, then have to use consumer.commit() method to manually commit.
                auto_commit_interval_ms=1000,  # Autocommit every second
                auto_offset_reset="earliest",
            )
            await consumer.start()

            logger.info(f"Kafka Consumer: Started")

            async for message in consumer:
                logger.info(f"Kafka Consumer: Key: {message.key} - Value: {message.value}")
                await consumer.commit()
        except Exception as e:
            logger.error(f"Exception: Kafka Consumer: {str(e)}")
        finally:
            await consumer.stop()


async def kafka_producer(message: str):
    producer = aiokafka.AIOKafkaProducer(
        bootstrap_servers="localhost:9092",
    )
    await producer.start()
    try:
        data = json.dumps({"data": message})
        logger.info(f"Kafka Producer: data : {data}")
        await producer.send_and_wait("send_notification", data.encode("utf-8"))
    except Exception as e:
        logger.error(f"Exception: Kafka Producer: {str(e)}")
    finally:
        await producer.stop()
