import asyncio
import typing as ty

import uvicorn

from lib.conf import config
from lib.db.db_instance import dbInstance
from lib.manager.routes import app as rest_app


def __init_uvicorn() -> None:
    @rest_app.on_event("shutdown")
    def shutdown() -> None:
        ...

    ssl_d: ty.Dict[ty.Any, ty.Any] = (
        {
            "ssl_keyfile": config.ssl_conn.SSL_KEY,
            "ssl_certfile": config.ssl_conn.SSL_CERT,
        }
        if config.SSL_ENABLED
        else {}
    )

    # TODO: add config and SSL connetion
    uvicorn_config = uvicorn.Config(
        rest_app,
        host=config.service.host,
        port=config.service.port,
        log_level=config.service.log_level,
        **ssl_d
    )

    server = uvicorn.Server(uvicorn_config)
    asyncio.get_event_loop().create_task(server.serve())


def main() -> None:
    __init_uvicorn()

    asyncio.get_event_loop().run_forever()
