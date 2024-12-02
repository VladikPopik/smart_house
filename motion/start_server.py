from src.db.mysql.motion_db.crud import create_record
import datetime, asyncio, time, json
from kafka_functions import produce_message_kafka, consume_message
from logging import getLogger

log = getLogger()

async def main():
    while True:
        log.info("Start cycle")
        try:
            produce_task = asyncio.create_task(produce_message_kafka("training_motion_topic"))
            await asyncio.gather(produce_task)
        

            consume_task = asyncio.create_task(consume_message())
            data = await asyncio.gather(consume_task)
            log.info(data)

        except Exception as e:
            print(e)
        time.sleep(5)

if __name__=="__main__":
    _loop = asyncio.new_event_loop()

    asyncio.get_event_loop().create_task(main())

    asyncio.get_event_loop().run_forever()
