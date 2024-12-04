from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from logging import getLogger
import datetime, json

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
        ) as consumer:  # pyright: ignore[reportGeneralTypeIssues]
            device = await consumer.getmany(timeout_ms=2500)
            first_device = next(iter(list(device.items())))
            el = first_device[1][-1]
            if el.value:
                data = json.loads(el.value)

            else:
                data = None
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
            logger.info(json.dumps("str"+"Данные отправлены в кафку"))
            print("Данные отправлены!")
    except Exception as e: 
        print(e) # noqa: BLE001
        _ = await producer.stop()
        logger.info(e)
        return False

    return True