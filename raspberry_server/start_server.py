import asyncio
import json
import typing as ty
# from concurrent.futures import ProcessPoolExecutor
from logging import getLogger, basicConfig, INFO
import datetime
from aiokafka import AIOKafkaProducer
from devices.monitoring import DhtSensor
from devices.motion import Capture
from devices.light import PhotoEl
from devices.utils import Error
import httpx

basicConfig(filename="server.log", level=INFO)
logger = getLogger(__name__)


type DeviceType = Capture | DhtSensor | PhotoEl

device_types = {"dht11": DhtSensor, "cam": Capture, "photoel": PhotoEl}


async def produce_device_result(
    _device: DeviceType,
    topic: str,
    value_to_send: dict[str, ty.Any],
    compression_type: str | None = None,
) -> bool:
    """Send result of perform_device into kafka by topic."""
    try:
        async with AIOKafkaProducer(
            bootstrap_servers="kafka:9092",
            request_timeout_ms=1000,
            max_request_size=2 * 75157290,
            compression_type=compression_type,
        ) as producer:
            _ = await producer.send(topic, value=json.dumps(value_to_send).encode())
            logger.info(topic)
            await producer.flush()
    except Exception as e:  # noqa: BLE001
        logger.error(e)
        return False
    return True


def dht(device: DhtSensor):
    try:
        result = device.read()
        return result
    except Exception as e:
        err = f"{e}"
        logger.error(err)
        logger.info(f"Dht11 result for {device}: {result}")  # noqa: G004


def cam(device: Capture):
    try:
        err, result = device.capture_camera()
        log_msg = f"Capture result for {device}: {True if result else False}"
        logger.info(log_msg)
        return err, result

    except Exception as e:
        logger.exception(e)
        result = []


def lux(device: PhotoEl):
    try:
        result = device.read()
        return result
    except Exception as e:
        logger.error(e)



# TODO: ADD PREV VALUES OUT OF EXECUTOR
def perform_device(device: DeviceType) -> tuple[Error, ty.Sequence]:
    try:
        match device.device_type:
            case "dht11":
                err, *result = dht(device=device)
                logger.info(f"Results {result}")  # noqa: G004
            case "photoel":
                err, *result = lux(device)
                logger.info(f"Results {result[0]}")
            case "cam":
                err, *result = cam(device)
            case _:
                raise ValueError("Unreachable!")
        return err, *result
    except Exception as e:
        logger.info(f"{e}")


async def produce(device: DeviceType, result, err) -> None:
    try:
        match device.device_type:
            case "dht11":
                _ = await produce_device_result(
                    device,
                    topic=f"{device.device_name}-{device.device_type}-rasp",
                    value_to_send={
                        "time": datetime.datetime.now().timestamp(),
                        "temperature": result[0],
                        "humidity": result[1],
                        "error": err,
                    },
                )
            case "photoel":
                _ = await produce_device_result(
                    device,
                    topic=f"{device.device_name}-{device.device_type}-rasp",
                    value_to_send={
                        "error": err,
                        "lux": result[0],
                        "infrared": result[1],
                        "visible": result[2],
                        "full_spectrum": result[3],
                    },
                )
            case "cam":
                _ = await produce_device_result(
                    device,
                    topic=f"{device.device_name}-{device.device_type}-rasp",
                    value_to_send={
                        "time": datetime.datetime.now().timestamp(),
                        "photos": result,
                        "error": err,
                    },
                    compression_type="gzip",
                )
    except Exception as e:
        logger.info(f"{e}")


async def get_registered_devices(timeout: int = 5000) -> httpx.Response:
    response: httpx.Response | None = None
    try:
        async with httpx.AsyncClient(timeout=5000) as client:
            while True:
                response = await client.get("http://backend:8001/settings/devices")
                if response and response.is_success:
                    return response
    except Exception as e:
        logger.exception(e)
        await asyncio.sleep(5)
        await get_registered_devices(timeout)

    await get_registered_devices(timeout)


async def connected_devices(devices_):
    for device in devices_:
        device_type = device["device_type"]
        if device["on"]:
            rasp_device: DeviceType = device_types[device_type](**device)
            yield rasp_device


async def main(time_to_cycle: int = 1, http_timeout: int = 5000) -> None:
    """Start raspberry server."""
    devices_: list[dict[str, ty.Any]] = []

    # with ProcessPoolExecutor(4) as executor:
    start = datetime.datetime.now().timestamp()

    response = await get_registered_devices(http_timeout)

    if response and response.is_success:
        devices_ = response.json()

    logger.info(devices_)

    async for device in connected_devices(devices_):  # noqa: PLC0206
        try:
            err, *result = perform_device(device) # await loop.run_in_executor(executor, perform_device, device)
            task = asyncio.create_task(produce(device, result, err))
            await asyncio.wait_for(task, timeout=60)
        except Exception as e:
            logger.exception(e)

    end = datetime.datetime.now().timestamp()

    consumed = end - start
    if consumed < time_to_cycle:
        await asyncio.sleep(time_to_cycle - consumed)
        end = datetime.datetime.now().timestamp()

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

    _loop.create_task(main(1))

    _loop.run_forever()
