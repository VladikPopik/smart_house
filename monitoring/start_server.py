from src.db.mysql.monit.crud import create_record
import asyncio
import json
import pickle
from kafka_functions import produce_message_kafka, consume_message
from logging import getLogger, basicConfig, INFO
import httpx
import datetime

basicConfig(filename="monitoring.log", level=INFO)
log = getLogger(__name__)

MODEL_PATH = "svr_temperature_model.pkl"

async def load_model(path):
    async with open(path, 'rb') as f:
        return pickle.load(f)

async def main(time_to_cycle=5):
    start = datetime.datetime.now().timestamp()
    try:
        async with httpx.AsyncClient() as client:
            while True:
                response = await client.get(
                    "http://backend:8001/settings/device/type/dht11",
                    params={"device_type": "dht11"}
                )
                if response.is_success:
                    break
            r = response.json()
            if not (r and r['device_name'] and r['device_type']):
                asyncio.get_running_loop().create_task(main(time_to_cycle))
            producer_topic = f"{r['device_name']}-{r['device_type']}"
            consumer_topic = producer_topic + "-rasp"
            log.info(f"{producer_topic}, {consumer_topic}")
    except Exception as e:
        log.error(e)
        raise httpx.NetworkError(f"{e}")

    try:
        log.info("Проверка захода в новый try/catch блок")
        data = await consume_message(consumer_topic)
        log.info(f"{data['time']} проверка на пенисность времени")
        log.info(f"{data['temperature']} проверка на пенисность температуры")
        # pickle.load("svr_temperature_model.pkl")
        result_inserting = await create_record(data)
        log.info(result_inserting)

        produce_task = await produce_message_kafka(producer_topic, data)
        # log.info(data)

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
