import asyncio
import datetime
import json
from logging import getLogger

from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter, WebSocket

from lib.utils import convert_error, Error

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
                        prev_t = data["temperature"]
                        prev_h = data["humidity"]
                        prev_t_pred_max, prev_t_pred_min = data["temperature"] + 5, data["temperature"] - 5
                        prev_h_pred_max, prev_h_pred_min = data["humidity"] + 5, data["humidity"] - 5
                        
                        error = data.get('error', Error.OK)
                        data.update({"error": convert_error('monitoring', error), "error_code": error})
                        
                        data.update(
                            {
                            "pred_temperature_max": prev_t_pred_max,
                            "pred_temperature_min": prev_t_pred_min,
                            "pred_humidity_max": prev_h_pred_max,
                            "pred_humidity_min": prev_h_pred_min,
                            }
                        )
                    else:
                        data = None
            if data is None:
                data = {
                    "time": datetime.datetime.now().timestamp(),
                    "temperature": prev_t,
                    "humidity": prev_h,
                    "pred_temperature_max": prev_t_pred_max,
                    "pred_temperature_min": prev_t_pred_min,
                    "pred_humidity_max": prev_h_pred_max,
                    "pred_humidity_min": prev_h_pred_min,
                    "error_code": Error.ERR_READ,
                    "error": convert_error("monitoring", Error.ERR_READ)
                }
        except Exception as e:  # noqa: BLE001
            logger.info(e)

        try:
            _ = await websocket.receive_text()
            await websocket.send_json(data)
        except Exception as e:  # noqa: BLE001
            logger.info(e)
            break
