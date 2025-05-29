import asyncio
import datetime
import json
from logging import getLogger

from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter, WebSocket

from lib.utils import convert_error, Error

from lib.db.mysql.settingsd import crud as cr

logger = getLogger()

light_router_ws = APIRouter()

@light_router_ws.websocket("/light_ws")
async def push_data_monitroing_ws(websocket: WebSocket) -> None:
    """WebSocket for light data."""
    await websocket.accept()
    type_d = "photoel"
    climates = await cr.read_device_by_type(type_d)
    topic = f"{climates['device_name']}-{climates['device_type']}" if climates else ""

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
                        error = data.get('error', Error.OK)
                        data.update({"error": convert_error('light', error), "error_code": error})
                        data.update({"time": datetime.datetime.now().timestamp()})
                    else:
                        data = None
        except Exception as e:  # noqa: BLE001
            logger.info(e)

        try:
            _ = await websocket.receive_text()
            await websocket.send_json(data)
        except Exception as e:  # noqa: BLE001
            logger.info(e)
            break
