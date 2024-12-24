import asyncio
import json
from kafka_functions import produce_message_kafka, consume_message
from logging import getLogger, basicConfig, INFO
import httpx
import datetime
from diod import Diod

basicConfig(filename="monitoring.log", level=INFO)
log = getLogger(__name__)

async def get_photoel(timeout: int=5000) -> httpx.Response:
    try:
        async with httpx.AsyncClient(timeout=5000) as client:
            response = await client.get(
                "http://backend:8001/settings/device/type/photoel",
                params={"device_type": "photoel"}
            )
        if response and response.is_success:
            return response
    except Exception as e:
        log.exception(e)
        await asyncio.sleep(5)
        await get_photoel(timeout)

async def main(time_to_cycle=5):
    start = datetime.datetime.now().timestamp()
    to_consume = False
    try:
        response = await get_photoel()

        if response.is_success:
            r = response.json()
            #Здесь у нас приходит запрос с бекенда если он не пустой и правильный 200 статус
            if r and r["on"]:
                #Сделал чтобы девайсы приходили в любом случае, но проверяем включен или нет
                producer_topic = f"{r['device_name']}-{r['device_type']}"
                consumer_topic = producer_topic + "-rasp"
                to_consume = True

            if to_consume:
                #Если девайс пришёл можно начинать слушать топики иначе идём в новый цикл и забиваем
                data = await consume_message(consumer_topic)
                time, percent = data.get("time"), data.get("percent")
                #Запускаем логику переключения диода
                diod.perform(percent)

                await produce_message_kafka(producer_topic, data)
    except Exception as e:
        log.error(e)

    end = datetime.datetime.now().timestamp()
    if end - start <= time_to_cycle:
        await asyncio.sleep(time_to_cycle - (end - start))

    log.info(f"Cycle elapsed after: {end - start} sec.")

    asyncio.get_running_loop().create_task(main(time_to_cycle))

if __name__=="__main__":
    _loop = asyncio.new_event_loop()
    log.info("Start work")

    #Пока что создаём один диод на 29 пине на плате! is_on=False так как думаю что всё должно быть выключено
    diod = Diod(29, "diod1", on=True, is_on=False)

    time_to_cycle = 10
    asyncio.get_event_loop().create_task(main(time_to_cycle))

    asyncio.get_event_loop().run_forever()
