import typing as ty
import asyncio

import uvicorn

from lib.utils import Singleton
from lib.manager.routes import app as rest_app


def __init_uvicorn() -> None:
	@rest_app.on_event("shutdown")
	def shutdown():
		pass


	#TODO: add config and SSL connetion
	uvicorn_config = uvicorn.Config(
		rest_app, host="127.0.0.1", port="8080", log_level='info'
	)

	server = uvicorn.Server(uvicorn_config)
	asyncio.get_event_loop().create_task(server.serve())




def main() -> None:
	__init_uvicorn()

	asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
	main()
