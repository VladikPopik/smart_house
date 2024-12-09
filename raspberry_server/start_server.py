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
import numpy as np

import httpx

basicConfig(filename="error.log", level=INFO)
logger = getLogger(__name__)


type DeviceType = Capture | DhtSensor
type DeviceReturnType = DhtReturnType | bool

device_types = {"dht11": DhtSensor, "cam": Capture}


async def produce_device_result(
    _device: DeviceType, topic: str, result: DeviceReturnType
) -> bool:
    """Send result of perform_device into kafka by topic."""
    try:
        async with AIOKafkaProducer(
            bootstrap_servers="kafka:9092",
            request_timeout_ms=1000
        ) as producer: # pyright: ignore[reportGeneralTypeIssues]
            value_to_send = {
                "time": datetime.datetime.now().timestamp(),
                "temperature": result[0],
                "humidity": result[1]
            }
            _ = await producer.send(
                topic, value=json.dumps(value_to_send).encode()
            )
            logger.info(json.dumps(value_to_send))
            logger.info(topic)
    except Exception as e:  # noqa: BLE001
        logger.info(e)
        return False

    return True


@singledispatch
def perform_device[
    T
](device: T) -> DeviceReturnType:  # pyright: ignore[reportInvalidTypeVarUse]
    """Generic function that gets result from every device type."""


@perform_device.register
def _(device: DhtSensor) -> DhtReturnType:
    result = (0.0, 0.0)
    try:
        result = device.read()
    except Exception as e:
        err = f"{e}"
        logger.exception(err)

    logger.info(f"Dht11 result for {device}: {result}")  # noqa: G004
    return np.random.randint(0, 100), np.random.random() # result # # result


@perform_device.register
def _(device: Capture) -> bool:
    try:
        result = device.capture_camera()
    except Exception as e:
        logger.exception(e)

    log_msg = f"Capture result for {device}: {result}"
    logger.info(log_msg)

    return result


def check_device(_device: DeviceType) -> bool:
    """Check whether device is connected or not."""
    return _device.on


async def main(time_to_cycle: int = 1) -> None:
    """Start raspberry server."""
    devices_: list[dict[str, ty.Any]] = []

    with ProcessPoolExecutor(4) as executor:
        start = datetime.datetime.now().timestamp()
        connected_devices: dict[str, DeviceType] = {}
        try:
            async with httpx.AsyncClient(timeout=5000) as client:
                response = await client.get(
                    "http://backend:8001/settings/devices"
                )
        except Exception as e:
            logger.exception(e)
            # await asyncio.sleep(time_to_cycle)
            # asyncio.get_running_loop().create_task(main(time_to_cycle))

        if response.is_success:
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
            _ = await produce_device_result(
                    d,
                    topic=f"{d.device_name}-{d.device_type}",
                    result=results[idx],
                )
        end = datetime.datetime.now().timestamp()

        if end - start <= time_to_cycle:
            await asyncio.sleep(time_to_cycle - (end - start))
        logger.info(f"This cycle has consumed {end - start} sec.")

        logger.info(f"Results {results}")  # noqa: G004
        logger.info(
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@STEP@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        )

        asyncio.get_running_loop().create_task(main(time_to_cycle))


if __name__ == "__main__":
    logger.info(
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@START UP@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    )

    #TODO @<VladikPopik>: wait for back to startup

    _loop = asyncio.new_event_loop()

    _loop.create_task(main(10))

    _loop.run_forever()
