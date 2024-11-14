import ast
import asyncio
import json
import typing as ty
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import singledispatch
from logging import getLogger, basicConfig, INFO

from aiokafka import AIOKafkaConsumer  # AIOKafkaProducer
from devices.monitoring import DhtReturnType, DhtSensor
from devices.motion import Capture


basicConfig(filename="error.log", level=INFO)
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
    result = None
    try:
        result = device.read()
    except Exception as e:
        logger.error(f"{e}")

    logger.info(f"Dht11 result for {device}: {result}")

    return result


@perform_device.register
def _(device: Capture) -> bool:
    try:
        result = device.capture_camera()
    except Exception as e:
        logger.error(f"{e}")

    logger.info(f"Capture result for {device}: {result}")
    return result


def check_device(_device: DeviceType) -> bool:
    """Check whether device is connected or not."""
    logger.info(f"{_device}, {_device.on}")
    return _device.on


async def fetch() -> dict[str, ty.Any] | None:
    """Function that gets device_data from kafka."""
    data = {}
    try:
        async with AIOKafkaConsumer(
            "test",
            bootstrap_servers="kafka:9092",
            auto_offset_reset="latest",
            connections_max_idle_ms=5000,
            session_timeout_ms=5000,
            request_timeout_ms=5000,
        ) as consumer:
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
    return data #{"device_name": "camera12", "voltage": 14, "device_type": "cam", "pin": 14, "on": True, "action": "update"} #data


async def main() -> None:
    """Start raspberry server."""
    devices_: list[DeviceType] = []
    connected_devices = {}

    with ProcessPoolExecutor(4) as executor:
        while True:
            task_fetch = asyncio.create_task(fetch())
            new_device_data_result = await asyncio.gather(task_fetch)
            new_device_data_result = new_device_data_result[0]
            deleted_name = None
            if new_device_data_result:
                device_type = new_device_data_result["device_type"]
                _ = new_device_data_result.pop("device_type", None)
                device_action = new_device_data_result["action"]
                _ = new_device_data_result.pop("action", None)
                if device_type in device_types:
                    #TODO @<VladikPopik>: test feature  # noqa: TD003
                    match device_action:
                        case "create":
                            device = device_types[device_type](**new_device_data_result)
                            devices_.append(device)
                        case "update":
                            is_in = False
                            for idx, dev in enumerate(devices_):
                                if dev.device_name == new_device_data_result["device_name"]:
                                    if device_type == "cam":
                                        devices_[idx].on = new_device_data_result["on"]
                                        devices_[idx].voltage = new_device_data_result["voltage"]
                                        devices_[idx].pin = new_device_data_result["pin"]
                                    devices_[idx] = device_types[device_type](**new_device_data_result)
                                    is_in = True
                                    break
                            if not is_in:
                                device = device_types[device_type](**new_device_data_result)
                                devices_.append(device)
                        case "delete":
                            delete_idx = None
                            for idx, dev in enumerate(devices_):
                                if dev.device_name == new_device_data_result["device_name"]:
                                    delete_idx = idx
                                    deleted_name = dev.device_name
                                    break
                            if delete_idx is not None:
                                devices_.pop(delete_idx)
                        case _:
                            msg = "Unreachable"
                            raise ValueError(msg)
                else:
                    logger.info(
                        f"No such device type as {device_type}"  # noqa: G004
                    )

            for device in devices_:
                _f = check_device(device)
                if _f:
                    connected_devices[device.device_name] = device

                if device.device_name in connected_devices and not _f:
                    del connected_devices[device.device_name]

            if deleted_name is not None:
                _ = connected_devices.pop(deleted_name, None)

            futures = []
            for c_device in connected_devices:
                device = connected_devices[c_device]
                logger.info(device)
                future = executor.submit(perform_device, device)
                futures.append(future)

            results = [f.result() for f in as_completed(futures)]
            logger.info(f"Results {results}")
            logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@STEP@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

if __name__ == "__main__":
    logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@START UP@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


    _loop = asyncio.new_event_loop()

    asyncio.get_event_loop().create_task(main())

    asyncio.get_event_loop().run_forever()
