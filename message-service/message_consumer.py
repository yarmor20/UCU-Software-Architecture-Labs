from aiokafka import AIOKafkaConsumer
from __logger import logger
from __constants import *

import uuid
import json
import asyncio


# In-memory message storage.
MESSAGES_MAP = dict()

# Create event loop for asynchronous kafka producer.
kafka_loop = asyncio.get_event_loop()


async def consume_messages():
    """
    Consume messages from Kafka topic and save them in RAM.
    """
    # Initialize a Kafka consumer.
    consumer = AIOKafkaConsumer(
        MESSAGE_SERVICE_KAFKA_TOPIC,
        loop=kafka_loop,
        bootstrap_servers=[KAFKA_BROKER],
        group_id=KAFKA_CONSUMER_GROUP
    )

    # Start consuming.
    await consumer.start()
    try:
        async for record in consumer:
            msg = json.loads(record.value)["message"]
            logger.info(f"(MESSAGE) Message recieved: [{msg}]")
            # Save message in map and commit to broker that message is recieved.
            MESSAGES_MAP[uuid.uuid1().__str__()] = msg
            await consumer.commit()

    except Exception as err:
        logger.error(f"(MESSAGE) Consumer error: [{err}]")
    finally:
        # Stop consuming.
        await consumer.stop()
