from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from logging import getLogger, basicConfig, INFO
import datetime, json

basicConfig(filename="error.log", level=INFO)
logger = getLogger(__name__)


async def consume_message(): 
    data = {}
    try:
        async with AIOKafkaConsumer(
            "test_topic_for_training",
            bootstrap_servers="kafka:9092",
            auto_offset_reset="latest",
            connections_max_idle_ms=5000,
            session_timeout_ms=5000,
            request_timeout_ms=5000,
        ) as consumer:  # pyright: ignore[reportGeneralTypeIssues]
            device = await consumer.getmany(timeout_ms=5000)
            first_device = next(iter(list(device.items())))
            el = first_device[1][-1]
            if el.value:
                data = json.loads(el.value)

            else:
                data = None

            await consumer.stop()  # pyright: ignore[reportGeneralTypeIssues]
    except Exception as e:
        logger.exception(e)
    return data


async def produce_message_kafka(topic:str) -> bool:
    try:
        async with AIOKafkaProducer(
            bootstrap_servers="kafka:9092",
        ) as producer:
            # value_to_send = {
            #     "time": datetime.datetime.now().timestamp(),
            #     "temperature": result[0],
            #     "humidity": result[1]
            # }
            value_to_send = {
                "time" : datetime.datetime.now().timestamp()
            }
            _ = await producer.send(
                topic, value=json.dumps(value_to_send).encode()
            )
            logger.info(json.dumps(str+"Данные отправлены в кафку"))
            print("Данные отправлены!")
    except Exception as e: 
        print(e) # noqa: BLE001
        _ = await producer.stop()
        logger.info(e)
        return False

    return True