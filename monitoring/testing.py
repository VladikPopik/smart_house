from library.db.mysql.monit.crud import create_record
import datetime
import asyncio
from library.conf.config_parser import Config


# kwargs = {
#     'username':'root',
#     'password':'admin',
#     'host':'0.0.0.0',
#     'port': '3306',
#     'database':'test'
# }

if __name__ == "__main__":
    # asyncio.get_event_loop().run_until_complete(create_record(datetime.datetime.now()))
    asyncio.run(create_record(datetime.datetime.now()))
