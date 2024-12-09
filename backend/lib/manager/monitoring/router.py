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
    topic = f"{climates["device_name"]}-{climates["device_type"]}-rasp" if climates else ""

    prev_t = 0.0
    prev_h = 0.0

    while True:
        try:
            el_data = None
            if topic:
                async with AIOKafkaConsumer(
                    topic,
                    bootstrap_servers="kafka:9092",
                    auto_offset_reset="latest",
                    connections_max_idle_ms=2500,
                    session_timeout_ms=2500,
                    request_timeout_ms=2500,
                    auto_commit_interval_ms=2500,
                ) as consumer:  # pyright: ignore[reportGeneralTypeIssues]
                    msg = await consumer.getmany(timeout_ms=2500)
                    first_device = next(iter(list(msg.items())))
                    print(msg.items())
                    el = first_device[1][-1]
                    if el.value:
                        el_data = json.loads(el.value)
                        el_data = ast.literal_eval(el_data)
                        prev_t = el_data["temperature"]
                        prev_h = el_data["humidity"]
            if el_data is None:
                el_data = {
                    "time": datetime.datetime.now().timestamp(),
                    "temperature": prev_t,
                    "humidity": prev_h
                }
        except Exception as e:  # noqa: BLE001
            logger.info(e)

        # logger.info(el_data)
        try:
            _ = await websocket.receive_text()
            await websocket.send_json(el_data)
            await asyncio.sleep(1)
        except Exception as e:  # noqa: BLE001
            logger.info(e)
            break
