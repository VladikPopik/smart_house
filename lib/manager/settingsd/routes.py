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


@settings_router.get("/devices", response_class=JSONResponse)  # , response_class=GetDevices # pyright: ignore[reportArgumentType]
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

@settings_router.get("/device")  # , response_class=GetDevice # pyright: ignore[reportArgumentType]
async def get_device(device_name: str) -> GetDevice:
    """API to get all devices from server."""
    result = await cr.device_read(device_name)
    return ty.cast(GetDevice, result)

@settings_router.post("/device") # , response_class=CreateDevice
async def create_device(params: CreateDevice) -> None:
    """API to create device."""
    await cr.create_device(params.model_dump())

@settings_router.delete("/device") #, response_class=DeleteDevice
async def device_delete(device_name: str) -> None:
    """API to delete device from server."""
    await cr.device_delete(device_name)


@settings_router.patch("/device") # , response_class=UpdateDevice
async def device_update(device_name: str, params: UpdateDevice) -> str:
    """API to update device by name."""
    return await cr.device_update(device_name=device_name, params=params.model_dump())
