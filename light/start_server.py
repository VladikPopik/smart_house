import asyncio
import json
from kafka_functions import produce_message_kafka, consume_message
from logging import getLogger
import httpx

log = getLogger(__name__)

async def get_photoel(timeout: int=5000) -> httpx.Response:
    try:
        async with httpx.AsyncClient(timeout=5000) as client:
            response = await client.get(
                "http://backend:8001/settings/device/type/photoel",
                params={"device_type": "photoel"}
            )
        return response
    except Exception as e:
        log.exception(e)
        await asyncio.sleep(1)
        await get_photoel(timeout)

async def main(time_to_cycle=5):
    try:
        response = await get_photoel()

        if response.is_success:
            r = response.json()
            producer_topic = f"{r['device_name']}-{r['device_type']}"
            consumer_topic = producer_topic + "-rasp"

            data = await consume_message(consumer_topic)
            time, percent = data.get("time"), data.get("percent")
            #Logic
            await produce_message_kafka(producer_topic, data)

    except Exception as e:
        log.error(e)
    
    await asyncio.sleep(time_to_cycle)

    asyncio.get_running_loop().create_task(main(time_to_cycle))

if __name__=="__main__":
    _loop = asyncio.new_event_loop()
    log.info("Start work")

    time_to_cycle = 5
    asyncio.get_event_loop().create_task(main(time_to_cycle))

    asyncio.get_event_loop().run_forever()
