import os
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

system_router = APIRouter()

@system_router.get("/pid")
async def get_pid():
    pid = os.getpid()
    return JSONResponse(
        jsonable_encoder(
            {"pid": pid}
        ),
        200
    )