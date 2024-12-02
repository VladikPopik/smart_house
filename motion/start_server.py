from src.db.mysql.motion_db.crud import create_record
import datetime, asyncio, time, json
from kafka_functions import produce_message_kafka, consume_message


async def main():
    while True:
        print("Start cycle")
        try:
            produce_task = asyncio.create_task(produce_message_kafka("training_motion_topic"))
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
