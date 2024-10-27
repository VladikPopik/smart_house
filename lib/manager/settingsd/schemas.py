from pydantic import BaseModel

class CreateDevice(BaseModel):
    device_name: str #length is 8-chars
    device_type: str
    voltage: float
    pin: int


class DeleteDevice(BaseModel):
    device_name: str


class UpdateDevice(BaseModel):
    device_type: str | None
    voltage: float | int
    pin: int | None


class GetDevice(BaseModel):
    device_name: str
    device_type: str
    voltage: float
    pin: int


class GetDevices(BaseModel):
    devices: list[GetDevice]
