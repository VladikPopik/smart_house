import ast
import asyncio
import datetime
import json
from logging import getLogger

from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter, WebSocket

from lib.db.mysql.settingsd import crud as cr

logger = getLogger()

motion_ws_router = APIRouter()


@motion_ws_router.websocket("/motion_ws")
async def push_data_motion_ws(websocket: WebSocket) -> None:
    """WebSocket for motion."""
    # await websocket.accept()
    # counter = 0
    # statuses = ["success", "warning", "info", "error"]
    # while True:
    #     try:
    #         ttx = await websocket.receive_text()
    #         # Send message to the client
    #         status = statuses[counter % 4]
    #         counter += 1
    #         print(status)
    #         resp = {"status": status, "time": time.time()}
    #         await websocket.send_json(resp)
    #         await asyncio.sleep(2)
    #     except Exception as e:
    #         print("error:", e)
    #         break
    await websocket.accept()
    type_d = "cam"
    climates = await cr.read_device_by_type(type_d)
    topic = f"{climates['device_name']}-{climates['device_type']-"rasp"}" if climates else ""

    while True:
        try:
            data = None
            if topic:
                async with AIOKafkaConsumer(
                    topic,
                    bootstrap_servers="kafka:9092",
                    auto_offset_reset="latest",
                    connections_max_idle_ms=2500,
                    session_timeout_ms=2500,
                    request_timeout_ms=2500,
                    auto_commit_interval_ms=2500,
                ) as consumer:
                    msg = await consumer.getone()
                    if msg and msg.value:
                        data = json.loads(msg.value)
                    else:
                        data = None
        except Exception as e:  # noqa: BLE001
            logger.info(e)

        try:
            _ = await websocket.receive_text()
            await websocket.send_json(data)
            await asyncio.sleep(1)
        except Exception as e:  # noqa: BLE001
            logger.info(e)
            break