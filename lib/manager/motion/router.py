from pathlib import Path
import time
import asyncio
from fastapi import WebSocket, APIRouter

import base64

motion_ws_router = APIRouter()

@motion_ws_router.websocket("/motion_ws")
async def push_data_motion_ws(websocket: WebSocket):
    await websocket.accept()
    counter = 0
    statuses = ["success", "warning", "info", "error"]
    while True:
        try:
            # Wait for any message from the client
            ttx = await websocket.receive_text()
            # Send message to the client
            status = statuses[counter % 4]
            counter += 1
            print(status)
            resp = {"status": status, "time": time.time()}
            await websocket.send_json(resp)
            await asyncio.sleep(2)
        except Exception as e:
            print("error:", e)
            break
