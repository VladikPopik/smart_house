import asyncio
import time
import typing as ty
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import singledispatch
from uuid import UUID

from devices.monitoring import DhtReturnType, DhtSensor
from devices.motion import Capture

type DeviceType = Capture | DhtSensor
type DeviceReturnType = DhtReturnType | bool

device_types = {"dht11": DhtSensor, "cam": Capture}


@singledispatch
def perform_device[
    T
](device: T) -> DeviceReturnType:  # pyright: ignore[reportInvalidTypeVarUse]
    """Generic function that gets result from every device type."""


@perform_device.register
def _(device: DhtSensor) -> DhtReturnType:
    try:
        result = device.read()
    except ValueError as e:
        print(e)  # noqa: T201
    return result


@perform_device.register
def _(device: Capture) -> bool:
    try:
        result = device.capture_camera()
    except ValueError as e:
        print(e)  # noqa: T201
    return result


def check_device(_device: DeviceType) -> bool:
    """Check whether device is connected or not."""
    return True


async def consumer() -> dict[str, ty.Any]:  # pyright: ignore[reportReturnType]
    """Create consumer and get data from kafka."""


async def producer(data: dict[str, ty.Any]) -> None:
    """Create producer to send mesages to kafka."""


async def wait_for_devices() -> dict[str, ty.Any] | None:
    """Function that gets device_data from kafka."""
    # TODO @<VladikPopik>: create consumer accepting data about devices  # noqa: TD003
    # device_data: dict[str, ty.Any] = await consumer()  # noqa: ERA001
    device_data = {"camport": 0, "type": "cam"}
    if device_data:
        return device_data

    return None


async def main(
    devices_: list[DeviceType], connected_devices: dict[UUID, DeviceType]
) -> tuple[list[DeviceReturnType], list[DeviceType], dict[UUID, DeviceType]]:
    """Service."""
    device_data = await wait_for_devices()
    if device_data:
        device_type = device_data["type"]
        device_data.pop("type", None)
        if device_type in device_types:
            device = device_types[device_type](**device_data)
            devices_.append(device)
        else:
            print(f"No such device type as {device_data["type"]}")  # noqa: T201
    else:
        print(f"No devices connected {devices_}")  # noqa: T201
        await wait_for_devices()

    for device in devices_:
        if device.uuid in connected_devices:
            continue

        _f = check_device(device)
        if _f:
            connected_devices[device.uuid] = device

    results = []
    with ProcessPoolExecutor(4) as executor:
        futures = []
        for c_device in connected_devices:
            device = connected_devices[c_device]
            future = executor.submit(perform_device, device)
            futures.append(future)

        results = [f.result() for f in as_completed(futures)]
        # TODO @<VladikPopik>: create producer to send messages to kafka by results  # noqa: TD003
        # if results:
        #     asyncio.run(producer(results))  # noqa: ERA001

    print(results)  # noqa: T201
    return results, devices_, connected_devices


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    devices_: list[DeviceType] = []
    connected_devices = {}
    while True:
        result, _devices_, _connected_devices = loop.run_until_complete(
            main(devices_, connected_devices)
        )
        time.sleep(5)
