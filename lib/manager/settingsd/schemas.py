from lib.utils.basemodel import Base


class CreateDevice(Base):
    device_name: str  # length is 8-chars
    device_type: str
    voltage: float
    pin: int
    on: bool | None = False


class DeleteDevice(Base):
    device_name: str


class UpdateDevice(Base):
    device_name: str
    device_type: str | None
    voltage: float | int
    pin: int | None
    on: bool | None = False


class GetDevice(Base):
    device_name: str
    device_type: str
    voltage: float
    pin: int


class GetDevices(Base):
    devices: list[GetDevice]
