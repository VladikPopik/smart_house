from library.db.mysql.monit.crud import create_record
from aiokafka import AIOKafkaProducer
import datetime, asyncio, time, json

from logging import getLogger, basicConfig, INFO


basicConfig(filename="error.log", level=INFO)
logger = getLogger(__name__)



async def produce_message_kafka(topic:str, message:datetime) -> bool:
    try:
        async with AIOKafkaProducer(
            bootstrap_servers="kafka:9092",
        ) as producer:
            # value_to_send = {
            #     "time": datetime.datetime.now().timestamp(),
            #     "temperature": result[0],
            #     "humidity": result[1]
            # }
            # value_to_send = {
            #     "time" : message
            # }
            _ = await producer.send(
                topic, value=json.dumps(message).encode()
            )
            logger.info(json.dumps(str+"Данные отправлены в кафку"))
            print("Данные отправлены!")
    except Exception as e: 
        print(e) # noqa: BLE001
        _ = await producer.stop()
        logger.info(e)
        return False

    return True


async def main():
    while True:
        print("Запущен процесс записи*****************")
        time_data = datetime.datetime.now()
        # _futures = []
        # _futures.append(asyncio.create_task(create_record(time_data)))
        # print('asdasdad')
        # _futures.append(asyncio.create_task(produce_message_kafka("test_topic_for_training", time_data)))
        # print(_futures)
        # _futures_send = await asyncio.gather(*_futures)
        # logger.info(f"Produced {_futures_send}")
        # _futures.clear()
        try:
            # asyncio.run(produce_message_kafka("test_topic_for_training", time_data))
            await produce_message_kafka("test_topic_for_training", time_data)
        except Exception as e:
            print(e)
        time.sleep(5)
        
        
    

if __name__=="__main__":
    _loop = asyncio.new_event_loop()

    asyncio.get_event_loop().create_task(main())

    asyncio.get_event_loop().run_forever()
