import asyncio
import time

import numpy as np
from fastapi import APIRouter, WebSocket

monitoring_router_ws = APIRouter()


@monitoring_router_ws.websocket("/monitoring_ws")
async def push_data_monitroing_ws(websocket: WebSocket) -> None:
    """WebSocket for monitoring data."""
    await websocket.accept()
    while True:
        try:
            _ttx = await websocket.receive_text()
            resp = {"value": np.random.random(), "time": time.time()}
            await websocket.send_json(resp)
            await asyncio.sleep(2)
        except Exception as e:
            print("error:", e)
            break
