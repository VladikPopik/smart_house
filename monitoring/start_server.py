from src.db.mysql.monit.crud import create_record, predict_next_temperatures, fetch_last_60_temps_for_prediction
import asyncio
import json
import pickle
import numpy
from kafka_functions import produce_message_kafka, consume_message
from logging import getLogger, basicConfig, INFO
import httpx
import datetime

basicConfig(filename="monitoring.log", level=INFO)
log = getLogger(__name__)

async def main(time_to_cycle=5):
    start = datetime.datetime.now().timestamp()
    to_consume = False
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
            to_consume = True
            log.info(f"{producer_topic}, {consumer_topic}")
    except Exception as e:
        log.error(e)
        raise httpx.NetworkError(f"{e}")

    try:
        if to_consume:
            try:
                data = await consume_message(consumer_topic)
                _ = await create_record(data)
                temperatures = await fetch_last_60_temps_for_prediction()
                log.info("После выборки с бд")
                log.info(temperatures)
                array_for_model = numpy.array(temperatures)
                predict =  await predict_next_temperatures(array_for_model)
                log.info("Предсказанная температура")
                log.info(predict)
            except Exception as e:
                log.error(e)
            finally:
                produce_task = await produce_message_kafka(producer_topic, data)
            # log.info(data)

    except Exception as e:
        log.error(e)

    end = datetime.datetime.now().timestamp()
    log.info(f"Cycle consumed: {end - start}")
    asyncio.get_running_loop().create_task(main(time_to_cycle))

if __name__=="__main__":
    _loop = asyncio.new_event_loop()

    log.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@START UP@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    time_to_cycle = 5

    _loop.create_task(main(time_to_cycle))

    _loop.run_forever()
