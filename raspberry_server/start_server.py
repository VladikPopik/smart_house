import asyncio
import time
import typing as ty
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import singledispatch
from uuid import UUID

import json
import ast
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from devices.monitoring import DhtReturnType, DhtSensor
from devices.motion import Capture

from logging import Logger

logger = Logger(__name__)



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


async def wait_for_devices() -> list[dict[str, ty.Any] | None]:
    """Function that gets device_data from kafka."""
    # TODO @<VladikPopik>: create consumer accepting data about devices  # noqa: TD003
    # device_data: dict[str, ty.Any] = await consumer()  # noqa: ERA001
    device_datas = []
    try:
        async with AIOKafkaConsumer(
                "test", bootstrap_servers="kafka:9092",
                auto_offset_reset="latest",
                connections_max_idle_ms=1000,
                session_timeout_ms=5000,
                request_timeout_ms=5000
        ) as consumer:
            logger.info("I'm here")
            device = await consumer.getone()
            if device.value:
                data = json.loads(device.value)
                data = ast.literal_eval(data)
            else:
                data = None
            device_datas.append(data)
    except Exception as e:
        logger.info(e)

    return device_datas


async def main(
    devices_: list[DeviceType],
    connected_devices: dict[UUID, DeviceType],
    executor: ProcessPoolExecutor,
) -> tuple[list[DeviceReturnType], list[DeviceType], dict[UUID, DeviceType]]:
    """Service."""
    device_datas = await wait_for_devices()
    for device_data in device_datas:
        if device_data:
            device_type = device_data["device_type"]
            _ = device_data.pop("device_type", None)
            if device_type in device_types:
                device = device_types[device_type](**device_data)
                devices_.append(device)
            else:
                logger.info(f"No such device type as {device_data["type"]}")  # noqa: T201

    logger.info(f"All devices are {devices_}")
    for device in devices_:
        if device.uuid in connected_devices:
            continue

        _f = check_device(device)
        if _f:
            connected_devices[device.uuid] = device

    results = []
    futures = []
    logger.info(f"Connected devices are: {connected_devices}")
    for c_device in connected_devices:
        device = connected_devices[c_device]
        logger.info(device)
        future = executor.submit(perform_device, device)
        futures.append(future)
        logger.info(f"Future {future}")
    results = [f.result() for f in as_completed(futures)]
    # TODO @<VladikPopik>: create producer to send messages to kafka by results  # noqa: TD003
    # if results:
    #     asyncio.run(producer(results))  # noqa: ERA001

    logger.info(results)  # noqa: T201
    return results, devices_, connected_devices


devices_: list[DeviceType] = []
connected_devices = {}

final_result = []

logger.info("READY FOR START UP")

with ProcessPoolExecutor(4) as executor:
    logger.info("PROCESSES CREATED INITIALIZING")
    while True:
        try:
            result, _devices_, _connected_devices = asyncio.run(
                main(devices_, connected_devices, executor)
            )
            final_result.append(result)
            final_result.pop(0)
            if len(devices_):
                devices_ = _devices_
                connected_devices = dict(_connected_devices)
            logger.info(connected_devices)
            logger.info(devices_)
            time.sleep(2)
            logger.info(final_result)  # noqa: T201
        except Exception as e:  # noqa: BLE001, PERF203
            print(f"{e}")  # noqa: T201
            break
