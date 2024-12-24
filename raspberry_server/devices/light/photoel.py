from uuid import UUID, uuid4
import RPi.GPIO as GPIO
import time
from devices.utils import Singleton


class PhotoEl(metaclass=Singleton):
    def __init__(
        self, pin: int, device_name: str, voltage: float, *, on: bool = False, device_type: str="photoel"
    ) -> None:
        self.device_name = device_name
        self.device_type = device_type
        self.uuid: UUID = uuid4()
        self.pin = pin
        self.voltage = voltage
        self.on = on
        self.time_to_cycle = 1

    def measure(self) -> tuple[float, int]:
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pin, GPIO.IN)
            cycle_time = time.time()
            while GPIO.input(self.pin) == 1:
                curr_time = time.time()
                if curr_time - cycle_time > self.time_to_cycle:
                    break

            pulse_start = time.time()
            while GPIO.input(self.pin) == 0:
                curr_time = time.time()
                if curr_time - pulse_start > self.time_to_cycle:
                    break
            
            pulse_end = time.time()
            
            pulse_duration = pulse_end - pulse_start
            total_duration = pulse_end - cycle_time
            
            duty_cycle = int(pulse_duration / total_duration * 100)
        finally:
            duty_cycle = -1
            GPIO.cleanup(self.pin)

        return time.time(), duty_cycle