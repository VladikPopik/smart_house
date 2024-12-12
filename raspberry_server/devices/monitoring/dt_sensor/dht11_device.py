from uuid import UUID, uuid4

import test_dht11 as test_dht11  # pyright: ignore[reportMissingTypeStubs]
from logging import getLogger
import RPi.GPIO as GPIO

import time
import datetime

type DhtReturnType = DHT11Result | None

logger = getLogger()

class DhtSensor[T]:
    """Class to handle DHT11 sensor working."""

    def __init__(
        self, pin: int, device_name: str, voltage: float, *, on: bool = False, device_type: str="dht11"
    ) -> None:
        self.device_name = device_name
        self.device_type = device_type
        self.uuid: UUID = uuid4()
        self.pin = pin
        self.voltage = voltage
        self.on = on
        self.instance = DHT11(pin=pin)

    def read(self) -> DhtReturnType:
        """Read data from dht11 sensor."""
        # GPIO.setmode(GPIO.BCM)
        result = self.instance.read()
        if result.is_valid():
            return result

        error = f"Cannot read from pin={self.pin} due to code number {result.error_code}, {result}"
        
        logger.error(error)
        
