import typing as ty

from uuid import UUID, uuid4

import random

from logging import getLogger
from devices.utils import Singleton

import datetime
import time


logger = getLogger()

class DHT11Result:
    'DHT11 sensor result returned by DHT11.read() method'

    ERR_NO_ERROR = 0
    ERR_MISSING_DATA = 1
    ERR_CRC = 2

    error_code = ERR_NO_ERROR
    temperature = -1
    humidity = -1

    def __init__(self, error_code, temperature, humidity):
        self.error_code = error_code
        self.temperature = temperature
        self.humidity = humidity

    def is_valid(self):
        return self.error_code == DHT11Result.ERR_NO_ERROR
    
    def __repr__(self) -> str:
        return f"t = {self.temperature}, h = {self.humidity}, err_code = {self.error_code}"


DhtReturnType: ty.TypeAlias = DHT11Result | None

class Dht11:
    def __init__(self, pin):
        self.pin = pin

    def read(self) -> DHT11Result:
        temperature = random.random() * 10 + 20 + random.random()
        humidity = random.random() * 10 + 30 + random.random()
        err = 0
        return DHT11Result(err, temperature=temperature, humidity=humidity)

class DhtSensor(metaclass=Singleton):
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
        self.instance = Dht11(pin=pin)
        self.prev_h = 0.0
        self.prev_t = 0.0

    def read(self) -> DhtReturnType:
        """Read data from dht11 sensor."""
        logger.info("Try to read instance")
        start = datetime.datetime.now().timestamp()
        while True:
            result = self.instance.read()
            if result.error_code == 0:
                self.prev_h = result.humidity
                self.prev_t = result.temperature
                # GPIO.cleanup(self.pin)
                return result

            end = datetime.datetime.now().timestamp()
            if end - start > 10:
                # GPIO.cleanup(self.pin)
                error = f"Cannot read from pin={self.pin} due to code number {result.error_code}, {result}"
                logger.error(error)
                return DHT11Result(1, float("-inf"), float("-inf"))