import ast
import asyncio
import datetime
import json
from logging import getLogger

import numpy as np

from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter, WebSocket

from lib.db.mysql.settingsd import crud as cr

logger = getLogger()

motion_ws_router = APIRouter()


@motion_ws_router.websocket("/motion_ws")
async def push_data_motion_ws(websocket: WebSocket) -> None:
    """WebSocket for motion."""
    await websocket.accept()
    type_d = "cam"
    cam = await cr.read_device_by_type(type_d)
    topic = f"{cam['device_name']}-{cam['device_type']}-rasp" if cam else ""

    while True:
        try:
            data = None
            print(topic)
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
                        consumed_data = json.loads(msg.value)
                        np_data = np.array(consumed_data['photos'][-1])
                        for idx, val in enumerate(np_data):
                            np_data[idx] = np.array(val, dtype=np.uint8)
                        data = {
                            "image": np_data.tobytes(),
                            "status": "success", 
                            "time": consumed_data["time"]
                        }
                    else:
                        data = None
        except Exception as e:  # noqa: BLE001
            print(e)

        try:
            _ = await websocket.receive_text()
            await websocket.send_json(data)
            await asyncio.sleep(1)
        except Exception as e:  # noqa: BLE001
            print(e)
            break