import RPi.GPIO as GPIO
from logging import getLogger

logger = getLogger()

class Diod:
    def __init__(
        self, pin: int, device_name: str, *,
        on: bool = False,
        device_type: str="diod",
        is_on = False
    ) -> None:
        self.device_name = device_name
        self.device_type = device_type
        self.pin = pin
        self.on = on
        self.is_on = is_on

    def switch_on(self) -> None:
        """Read data from dht11 sensor."""
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pin, GPIO.OUT)
            logger.info(f"{self.device_name}: led on")
            GPIO.output(self.pin, GPIO.HIGH)
            self.is_on = True
        except Exception as e:
            logger.exception(f"{e}")

    def switch_off(self) -> None:
        try:
            GPIO.output(self.pin, GPIO.LOW)
            logger.info(f"{self.device_name}: led off")
        except Exception as e:
            logger.exception(f"{e}")
        finally:
            GPIO.cleanup(self.pin)

        self.is_on = False

    def perform(self, time, percent) -> None:
        try:
            if percent <= 50 and not self.is_on:
                self.switch_on()
            elif percent > 50 and self.is_on:
                self.switch_off()
            else:
                return
        except Exception as e:
            logger.exception(f"{e}")