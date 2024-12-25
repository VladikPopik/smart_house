from src.db.mysql.monit.crud import create_record, get_records_batch
import asyncio
import joblib
import numpy as np
from kafka_functions import produce_message_kafka, consume_message
from logging import getLogger, basicConfig, INFO
import httpx
import datetime

basicConfig(filename="monitoring.log", level=INFO)
log = getLogger(__name__)

batch_size = 20 
current_offset = 0 

#Загрузка модели SVR
model = joblib.load('/monitoring/svr_temperature_model.joblib')

async def main(time_to_cycle=5):
    global current_offset
    log.info("Start work")
    start = datetime.datetime.now().timestamp()

    #Запрос для получения названия топика кафки
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://backend:8001/settings/device/type/dht11",
                params={"device_type": "dht11"}
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
        #Чтение топика с данными с датчика
        data = await consume_message(consumer_topic)

        #Запись полученных данных в бд
        _ = await create_record(time=data.get('time', None), temperature=data.get('temperature', None), humidity=data.get('humidity', None))


        records, current_offset = await get_records_batch(batch_size, current_offset)
        if records:
            log.info(f"Обработано {len(records)} записей.")
            temperatures = [record['temperature'] for record in records if record.get('temperature') is not None]

            if len(temperatures) == batch_size:

                # Приведение данных в нормальный вид для модели
                X = np.array(temperatures).reshape(-1, 1)

                # Предсказание модели
                predicted_temperatures = model.predict(X)

                # Расчет +-5% от предсказанных значений
                temperature_ranges = {
                    'predicted': predicted_temperatures.tolist(),
                    'upper_bound': (predicted_temperatures * 1.05).tolist(),
                    'lower_bound': (predicted_temperatures * 0.95).tolist(),
                }

                messages = []
                for record, predicted_temp, upper, lower in zip(records, predicted_temperatures, temperature_ranges['upper_bound'], temperature_ranges['lower_bound']):
                    # Формируем сообщение для продюсера кафки
                    message = {
                        'real_temperature': record.get('temperature', None),
                        'humidity': record.get('humidity', None),
                        'time': data.get('time', None), 
                        'predicted_temperature': predicted_temp,
                        'upper_bound': upper,
                        'lower_bound': lower,
                    }
                    messages.append(message)

                # Отправляем все сообщения в Kafka
                for message in messages:
                    produce_task = await produce_message_kafka(producer_topic, message)
                    log.info(f"Sent message: {message}")

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
