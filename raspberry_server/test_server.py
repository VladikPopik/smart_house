import ast
import asyncio
import json
import time
import typing as ty
from collections.abc import Generator
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import singledispatch
from logging import getLogger

from aiokafka import AIOKafkaConsumer  # AIOKafkaProducer
from devices.monitoring import DhtReturnType, DhtSensor
from devices.motion import Capture
from tqdm import tqdm

logger = getLogger(__name__)


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
    return True # _device.on


async def fetch() -> dict[str, ty.Any] | None:
    """Function that gets device_data from kafka."""
    data = {}
    try:
        async with AIOKafkaConsumer(
            "test",
            bootstrap_servers="kafka:9092",
            auto_offset_reset="latest",
            connections_max_idle_ms=1000,
            session_timeout_ms=5000,
            request_timeout_ms=5000,
        ) as consumer:
            logger.info("I'm here")
            device = await consumer.getmany(timeout_ms=5000)
            first_device = next(iter(list(device.items())))
            el = first_device[1][0]
            if el.value:
                data = json.loads(el.value)
                data = ast.literal_eval(data)
            else:
                data = None

            await consumer.stop() # pyright: ignore[reportGeneralTypeIssues]
    except Exception as _e:  # noqa: BLE001
        logger.info("Cannot read from topic 'test'")

    return data  # {"device_name": "camera12", "voltage": 14, "device_type": "cam", "pin": 14, "on": True} #data


def generator() -> Generator[None, None, None]:
    """While true."""
    while True:
        yield


async def main() -> None:
    """Start raspberry server."""
    devices_: list[DeviceType] = []
    connected_devices = {}

    with ProcessPoolExecutor(4) as executor:
        for _ in tqdm(generator()):
            task_fetch = asyncio.create_task(fetch())
            new_device_data_result = await asyncio.gather(task_fetch)
            new_device_data_result = new_device_data_result[0]

            if new_device_data_result:
                device_type = new_device_data_result["device_type"]
                _ = new_device_data_result.pop("device_type", None)
                device_action = new_device_data_result["action"]
                _ = new_device_data_result.pop("action", None)

                deleted_uuid = None
                if device_type in device_types:
                    #TODO @<VladikPopik>: test feature
                    match device_action:
                        case "create":
                            device = device_types[device_type](**new_device_data_result)
                            devices_.append(device)
                        case "update":
                            for dev in devices_:
                                if dev.device_name == new_device_data_result["device_name"]:
                                    device = dev
                                else:
                                    device = device_types[device_type](**new_device_data_result)
                                    devices_.append(device)
                        case "delete":
                            delete_idx = None
                            for idx, dev in enumerate(devices_):
                                if dev.device_name == new_device_data_result["device_name"]:
                                    delete_idx = idx
                                    deleted_uuid = dev.uuid
                            if delete_idx is not None:
                                devices_.pop(delete_idx)
                        case _:
                            msg = "Unreachable"
                            raise ValueError(msg)
                else:
                    logger.info(
                        f"No such device type as {new_device_data_result["type"]}"  # noqa: G004
                    )

            logger.info(f"All devices are {devices_}")  # noqa: G004
            for device in devices_:
                _f = check_device(device)
                if _f:
                    connected_devices[device.uuid] = device

            if deleted_uuid is not None:
                _ = connected_devices.pop(deleted_uuid, None)

            futures = []
            logger.info(
                f"Connected devices are: {connected_devices}"  # noqa: G004
            )
            for c_device in connected_devices:
                device = connected_devices[c_device]
                logger.info(device)
                future = executor.submit(perform_device, device)
                futures.append(future)
                logger.info(f"Future {future}")  # noqa: G004

            results = [f.result() for f in as_completed(futures)]
            logger.info(results)
            time.sleep(1)  # noqa: ASYNC251


if __name__ == "__main__":
    logger.info("START UP")

    for _i in tqdm(range(100)):
        ...
    _loop = asyncio.new_event_loop()

    asyncio.get_event_loop().create_task(main())

    asyncio.get_event_loop().run_forever()
