import ast
import asyncio
import datetime
import json
from logging import getLogger

from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter, WebSocket

from lib.db.mysql.settingsd import crud as cr

logger = getLogger()

monitoring_router_ws = APIRouter()


@monitoring_router_ws.websocket("/monitoring_ws")
async def push_data_monitroing_ws(websocket: WebSocket) -> None:
    """WebSocket for monitoring data."""
    await websocket.accept()
    type_d = "dht11"
    climates = await cr.read_device_by_type(type_d)
    topic = f"{climates['device_name']}-{climates['device_type']}" if climates else ""

    prev_t = 0.0
    prev_h = 0.0

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
                        prev_t = data["temperature"] if data["temperature"] else prev_t
                        prev_h = data["humidity"] if data["humidity"] else prev_h
                    else:
                        data = None
            if data is None:
                data = {
                    "time": datetime.datetime.now().timestamp(),
                    "temperature": prev_t,
                    "humidity": prev_h
                }
        except Exception as e:  # noqa: BLE001
            logger.info(e)

        try:
            _ = await websocket.receive_text()
            await websocket.send_json(data)
            await asyncio.sleep(1)
        except Exception as e:  # noqa: BLE001
            logger.info(e)
            break
