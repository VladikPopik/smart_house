from src.db.mysql.monit.crud import create_record
import asyncio
import json
from kafka_functions import produce_message_kafka, consume_message
from logging import getLogger, basicConfig, INFO
import httpx
import datetime

basicConfig(filename="motion.log", level=INFO)
log = getLogger(__name__)

async def main(time_to_cycle=5):
    log.info("Start work")
    start = datetime.datetime.now().timestamp()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://backend:8001/settings/device/type/cam",
                params={"device_type": "cam"}
            )
        if response.is_success:
            r = response.json()
            producer_topic = f"{r['device_name']}-{r['device_type']}"
            consumer_topic = producer_topic + "-rasp"
            log.info(f"{producer_topic}, {consumer_topic}")
    except Exception as e:
        log.error(e)
        raise httpx.NetworkError(f"{e}")

    try:
        data = await consume_message(consumer_topic)

        produce_task = await produce_message_kafka(producer_topic, data)
        log.info(data)

    except Exception as e:
        log.error(e)

    end = datetime.datetime.now().timestamp()
    if end - start < time_to_cycle:
        await asyncio.sleep(time_to_cycle - (end - start))

    asyncio.get_running_loop().create_task(main(time_to_cycle))

if __name__=="__main__":
    _loop = asyncio.new_event_loop()

    log.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@START UP@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    time_to_cycle = 5

    _loop.create_task(main(time_to_cycle))

    _loop.run_forever()
