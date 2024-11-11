import asyncio

import uvicorn

from src import app as rest_app
from config import CONFIG_PORT, CONFIG_HOST, CONFIG_LOG_LEVEL
from aiokafka import AIOKafkaConsumer

def __init_uvicorn() -> None:
    @rest_app.on_event("shutdown")
    def shutdown() -> None: ...

    @rest_app.on_event("startup")
    async def startup_event():
        loop = asyncio.get_event_loop()
        print("NEW TASK")
        cons = AIOKafkaConsumer(
                "test", bootstrap_servers="kafka:9092"
        )
        t = [loop.create_task(cons.getone()) for i in range(2)]
        # print(t.as())
        res = asyncio.as_completed(t)
        # print([await r for r in res])
        print("TASK COMPLETED")


    # TODO (VladikPopik): add config and SSL connetion  # noqa: TD003
    uvicorn_config = uvicorn.Config(
        rest_app,
        host=CONFIG_HOST,
        port=CONFIG_PORT,
        log_level=CONFIG_LOG_LEVEL,
    )

    server = uvicorn.Server(uvicorn_config)
    asyncio.get_event_loop().create_task(server.serve())

def main() -> None:
    """Run backend service."""
    __init_uvicorn()

    asyncio.get_event_loop().run_forever()
