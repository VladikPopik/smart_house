import json
import typing as ty
from pydantic import BaseModel, model_validator


class Base(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def model_validate_json(
        cls,
        json_data: str | bytes | bytearray,
        *,
        strict: bool | None = None,
        context: ty.Any | None = None
    ) -> ty.Self:
        if isinstance(json_data, str) or isinstance(json_data, bytes):
            return cls(**json.loads(json_data))
        return json_data


class CreateDevice(Base):
    device_name: str #length is 8-chars
    device_type: str
    voltage: float
    pin: int


class DeleteDevice(Base):
    device_name: str


class UpdateDevice(Base):
    device_name: str
    device_type: str | None
    voltage: float | int
    pin: int | None


class GetDevice(Base):
    device_name: str
    device_type: str
    voltage: float
    pin: int


class GetDevices(Base):
    devices: list[GetDevice]
