import asyncio
import json
import typing as ty
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import singledispatch
from logging import getLogger, basicConfig, INFO
import datetime
from aiokafka import AIOKafkaProducer
from devices.monitoring import DhtReturnType, DhtSensor
from devices.motion import Capture
from devices.light import PhotoEl
import numpy as np

import httpx

basicConfig(filename="error.log", level=INFO)
logger = getLogger(__name__)


type DeviceType = Capture | DhtSensor | PhotoEl
type DeviceReturnType = DhtReturnType | dict[str, str] | tuple[float, int]

device_types = {"dht11": DhtSensor, "cam": Capture, "photoel": PhotoEl}


async def produce_device_result(
    _device: DeviceType,
    topic: str,
    value_to_send: dict[str, ty.Any],
    compression_type: str | None = None
) -> bool:
    """Send result of perform_device into kafka by topic."""
    try:
        async with AIOKafkaProducer(
            bootstrap_servers="kafka:9092",
            request_timeout_ms=1000,
            max_request_size=2*75157290,
            compression_type=compression_type
        ) as producer:
            _ = await producer.send(
                topic, value=json.dumps(value_to_send).encode()
            )
            # logger.info(json.dumps(value_to_send))
            logger.info(topic)
            await producer.flush()
    except Exception as e:  # noqa: BLE001
        logger.error(e)
        return False
    return True

@singledispatch
def perform_device[
    T
](device: T) -> DeviceReturnType:  # pyright: ignore[reportInvalidTypeVarUse]
    """Generic function that gets result from every device type."""

@perform_device.register
def _(device: DhtSensor) -> DhtReturnType | tuple[float, float]:
    try:
        result = device.read()
    except Exception as e:
        err = f"{e}"
        logger.error(err)

    logger.info(f"Dht11 result for {device}: {result}")  # noqa: G004
    return (result.temperature, result.humidity)

@perform_device.register
def _(device: Capture) -> dict[str, ty.Any]:
    try:
        result = device.capture_camera()
    except Exception as e:
        logger.exception(e)
        result = []

    log_msg = f"Capture result for {device}: {True if result else False}"
    logger.info(log_msg)

    return result

@perform_device.register
def _(device: PhotoEl) -> tuple[float, int]:
    try:
        result = device.measure()
    except Exception as e:
        logger.error(e)

    return result

async def get_registered_devices(timeout: int=5000) -> httpx.Response:
    response: httpx.Response | None = None
    try:
        async with httpx.AsyncClient(timeout=5000) as client:
            response = await client.get(
                "http://backend:8001/settings/devices"
            )
    except Exception as e:
        logger.exception(e)
        await asyncio.sleep(5)
        await get_registered_devices(timeout)

    if response and response.is_success:
        return response
    await get_registered_devices(timeout)


async def main(time_to_cycle: int = 1, http_timeout: int=5000) -> None:
    """Start raspberry server."""
    devices_: list[dict[str, ty.Any]] = []

    with ProcessPoolExecutor(4) as executor:
        start = datetime.datetime.now().timestamp()
        connected_devices: dict[str, DeviceType] = {}

        response = await get_registered_devices(http_timeout)

        if response and response.is_success:
            devices_ = response.json()

        logger.info(devices_)

        for device in devices_:
            device_type = device["device_type"]
            if device["on"]:
                rasp_device = device_types[device_type](**device)
                connected_devices[rasp_device.device_name] = rasp_device

        futures = []
        t_devices = []
        for c_device in connected_devices:  # noqa: PLC0206
            device = connected_devices[c_device]
            future = executor.submit(perform_device, device)
            futures.append(future)
            t_devices.append(device)

        results = [f.result() for f in as_completed(futures)]
        for idx, d in enumerate(t_devices):
            try:
                match d.device_type:
                    case "dht11":
                        _ = await produce_device_result(
                                d,
                                topic=f"{d.device_name}-{d.device_type}-rasp",
                                value_to_send = {
                                    "time": datetime.datetime.now().timestamp(),
                                    "temperature": results[idx][0],
                                    "humidity": results[idx][1]
                                }
                            )
                        logger.info(f"Results {results}")  # noqa: G004
                    case "photoel":
                        _ = await produce_device_result(
                            d,
                            topic=f"{d.device_name}-{d.device_type}-rasp",
                            value_to_send = {
                                "time": results[idx][0],
                                "percent": results[idx][1]
                            }
                        )
                        logger.info(f"Results {results}")
                    case "cam":
                        logger.info(type(results[idx]))
                        _ = await produce_device_result(
                            d,
                            topic=f"{d.device_name}-{d.device_type}-rasp",
                            value_to_send = {
                                "time": datetime.datetime.now().timestamp(),
                                "photos": results[idx]
                            },
                            compression_type='gzip'
                        )
                    case _:
                        raise ValueError("Unreachable!")
            except Exception as e:
                logger.info(f"{e}")
                
        end = datetime.datetime.now().timestamp()

        if end - start <= time_to_cycle:
            await asyncio.sleep(time_to_cycle - (end - start))
        logger.info(f"This cycle has consumed {end - start} sec.")

        logger.info(
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@STEP@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        )

        asyncio.get_running_loop().create_task(main(time_to_cycle))


if __name__ == "__main__":
    logger.info(
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@START UP@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    )

    _loop = asyncio.new_event_loop()

    _loop.create_task(main(10))

    _loop.run_forever()
