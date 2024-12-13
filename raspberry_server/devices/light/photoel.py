from uuid import UUID, uuid4
import RPi.GPIO as GPIO
import datetime
import numpy as np


class PhotoEl:
    def __init__(
        self, pin: int, device_name: str, voltage: float, *, on: bool = False, device_type: str="dht11"
    ) -> None:
        self.device_name = device_name
        self.device_type = device_type
        self.uuid: UUID = uuid4()
        self.pin = pin
        self.voltage = voltage
        self.on = on

    def read(self) -> tuple[float, float]:
        return (datetime.datetime.now().timestamp(), np.random.rand())