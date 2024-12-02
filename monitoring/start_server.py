from library.db.mysql.monit.crud import create_record
import datetime, asyncio, time, json
from kafka_functions import produce_message_kafka, consume_message



async def main():
    while True:
        print("Start work")
        # time_data = datetime.datetime.now()
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
            # await produce_message_kafka("test_topic_for_training")
            produce_task = asyncio.create_task(produce_message_kafka("test_topic_for_training"))
            await asyncio.gather(produce_task)
        

            consume_task = asyncio.create_task(consume_message())
            data = await asyncio.gather(consume_task)
            print(data)

        except Exception as e:
            print(e)
        time.sleep(5)

if __name__=="__main__":
    _loop = asyncio.new_event_loop()

    asyncio.get_event_loop().create_task(main())

    asyncio.get_event_loop().run_forever()
