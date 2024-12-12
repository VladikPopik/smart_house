from uuid import UUID, uuid4

from .test_dht11 import DHT11, DHT11Result  # pyright: ignore[reportMissingTypeStubs]
from logging import getLogger
import RPi.GPIO as GPIO
from devices.utils import Singleton

import datetime
import time

type DhtReturnType = DHT11Result | None

logger = getLogger()

class DhtSensor(metaclass=Singleton):
    """Class to handle DHT11 sensor working."""
    prev_t, prev_h = 0.0, 0.0


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
        GPIO.setmode(GPIO.BOARD)
        start = datetime.datetime.now().timestamp()
        while True:
            result = self.instance.read()

            if result.error_code == 0:
                self.prev_h = result.humidity
                self.prev_t = result.temperature
                GPIO.cleanup()
                return result

            end = datetime.datetime.now().timestamp()
            if end - start > 30:
                GPIO.cleanup()
                return DHT11Result(0, self.prev_t, self.prev_h)
            time.sleep(1)

            error = f"Cannot read from pin={self.pin} due to code number {result.error_code}, {result}"
            logger.error(error)

