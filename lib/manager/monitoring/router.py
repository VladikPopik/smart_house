import numpy as np
import time
import asyncio
from fastapi import WebSocket, APIRouter

monitoring_router_ws = APIRouter()


@monitoring_router_ws.websocket("/monitoring_ws")
async def push_data_monitroing_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Wait for any message from the client
            ttx = await websocket.receive_text()
            print(ttx)
            # Send message to the client
            resp = {"value": np.random.random(), "time": time.time()}
            print(resp)
            await websocket.send_json(resp)
            await asyncio.sleep(2)
        except Exception as e:
            print("error:", e)
            break
