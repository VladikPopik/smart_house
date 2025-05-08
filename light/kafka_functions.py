from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from logging import getLogger
import json
import typing as ty

logger = getLogger()

async def consume_message(topic: str) -> dict[str, ty.Any]: 
    data = {}
    try:
        async with AIOKafkaConsumer(
            topic,
            bootstrap_servers="kafka:9092",
            auto_offset_reset="latest",
            connections_max_idle_ms=5000,
            session_timeout_ms=5000,
            request_timeout_ms=5000,
        ) as consumer:
            device = await consumer.getone()
            if device:
                data = json.loads(device.value)
            else:
                data = None
    except Exception as e:
        logger.exception(e)
    return data


async def produce_message_kafka(topic:str, data: dict[str, ty.Any]) -> bool:
    try:
        async with AIOKafkaProducer(
            bootstrap_servers="kafka:9092",
        ) as producer:
            _ = await producer.send(
                topic, value=json.dumps(data).encode()
            )
    except Exception as e: 
        print(e) # noqa: BLE001
        _ = await producer.stop()
        logger.info(e)
        return False

    return True