import RPi.GPIO as GPIO

class Diod:
    def __init__(
        self, pin: int, device_name: str, *, on: bool = False, device_type: str="diod"
    ) -> None:
        self.device_name = device_name
        self.device_type = device_type
        self.pin = pin
        self.on = on

    def on(self):
        """Read data from dht11 sensor."""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        print("led on")
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.OUT)
        print("led off")
        GPIO.cleanup()
