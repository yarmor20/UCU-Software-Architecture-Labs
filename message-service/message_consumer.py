from aiokafka import AIOKafkaConsumer
from __logger import logger
from __constants import *
from __utils import *

import uuid
import json
import asyncio


# In-memory message storage.
MESSAGES_MAP = dict()

# Create event loop for asynchronous kafka producer.
kafka_loop = asyncio.get_event_loop()


async def consume_messages(cclient) -> None:
    """
    Consume messages from Kafka topic and save them in RAM.

    :param cclient: (consul.Client) - Consul client agent.
    """
    # Get Kafka configurations from Consul KV storage.
    broker = get_consul_value(cclient, key=KAFKA_BROKER_KEY)
    consumer_group = get_consul_value(cclient, key=KAFKA_CONSUMER_GROUP_KEY)
    topic = get_consul_value(cclient, key=MESSAGE_SERVICE_KAFKA_TOPIC_KEY)

    # Initialize a Kafka consumer.
    consumer = AIOKafkaConsumer(
        topic,
        loop=kafka_loop,
        bootstrap_servers=[broker],
        group_id=consumer_group
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
