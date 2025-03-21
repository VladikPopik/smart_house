from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from logging import getLogger
import json
import typing as ty

logger = getLogger()

async def consume_message(topic: str): 
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


async def produce_result(
    topic: str,
    value_to_send: dict[str, ty.Any],
    compression_type: str | None = None,
) -> bool:
    """Send result of perform_device into kafka by topic."""
    try:
        async with AIOKafkaProducer(
            bootstrap_servers="kafka:9092",
            request_timeout_ms=1000,
            max_request_size=2*75157290,
            compression_type=compression_type
        ) as producer:
            _ = await producer.send(
                topic, value=json.dumps(value_to_send).encode()
            )
            logger.info(topic)
            await producer.flush()
    except Exception as e:  # noqa: BLE001
        logger.error(e)
        return False
    return True