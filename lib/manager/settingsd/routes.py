import typing as ty

from lib.db.mysql.settingsd import crud as cr
from .schemas import (
    GetDevice,
    GetDevices,
    UpdateDevice,
    DeleteDevice,
    CreateDevice
)

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

settings_router = APIRouter()


@settings_router.get("/devices", response_class=JSONResponse)
async def get_all_devices() -> JSONResponse:
    """API to get all devices from server."""
    try:
        result = await cr.read_all()
        return JSONResponse(jsonable_encoder(result), 200)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            400, 
            detail=e
        )

@settings_router.get("/device")
async def get_device(device_name: str) -> JSONResponse:
    """API to get all devices from server."""
    result = await cr.device_read(device_name)
    return JSONResponse(jsonable_encoder(result), 200)

@settings_router.post("/device")
async def create_device(params: CreateDevice) -> JSONResponse:
    """API to create device."""
    await cr.create_device(params.model_dump())
    return JSONResponse(content="OK", status_code=200)

@settings_router.delete("/device")
async def device_delete(device_name: str) -> JSONResponse:
    """API to delete device from server."""
    await cr.device_delete(device_name)
    return JSONResponse(content="OK", status_code=200)



@settings_router.patch("/device")
async def device_update(params: UpdateDevice) -> JSONResponse:
    """API to update device by name."""
    result = await cr.device_update(device_name=params.device_name, params=params.model_dump(exclude={"device_name"}))
    return JSONResponse(jsonable_encoder(result), 200)
