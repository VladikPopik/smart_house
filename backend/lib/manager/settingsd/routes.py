import typing as ty

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from lib.db.mysql.settingsd import crud as cr
from lib.KafkaMsg.producers import JSONProducer

from .schemas import (CreateDevice, DeleteDevice, GetDevice, GetDevices,
                      UpdateDevice)

settings_router = APIRouter()


@settings_router.get("/devices", response_class=JSONResponse)
async def get_all_devices() -> JSONResponse:
    """API to get all devices from server."""
    try:
        result = await cr.read_all()
        return JSONResponse(jsonable_encoder(result), 200)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(400, detail=e)


@settings_router.get("/device")
async def get_device(device_name: str) -> JSONResponse:
    """API to get all devices from server."""
    result = await cr.device_read(device_name)
    return JSONResponse(jsonable_encoder(result), 200)


@settings_router.post("/device")
async def create_device(params: CreateDevice) -> JSONResponse:
    """API to create device."""
    res = {}
    await cr.create_device(params.model_dump())
    async with JSONProducer().get_producer() as producer:
        v = params.model_dump()
        v["action"] = "create"
        res = await producer.send("test", f"{v}")
    return JSONResponse(content=f"{res}", status_code=200)


@settings_router.delete("/device")
async def device_delete(device_name: str) -> JSONResponse:
    """API to delete device from server."""
    device = await cr.device_read(device_name=device_name)
    await cr.device_delete(device_name)
    res = {}
    async with JSONProducer().get_producer() as producer:
        if device:
            v = dict(device)
            v["action"] = "delete"
            res = await producer.send("test", f"{v}")
    return JSONResponse(content=f"{res}", status_code=200)


@settings_router.patch("/device")
async def device_update(params: UpdateDevice) -> JSONResponse:
    """API to update device by name."""
    result = await cr.device_update(
        device_name=params.device_name,
        params=params.model_dump(exclude={"device_name"}),
    )
    device = await cr.device_read(params.device_name)
    async with JSONProducer().get_producer() as producer:
        if device:
            v = dict(device)
            v["action"] = "update"
            print(f"{v}")
            res = await producer.send("test", f"{v}")
    return JSONResponse(jsonable_encoder(result), 200)


@settings_router.get("/device/{type}")
async def get_device_by_type(device_type: str) -> str | None:
    result = await cr.read_device_by_type(device_type)

    if result["device_type"] is not None:
        return result["device_type"]
    
    return None