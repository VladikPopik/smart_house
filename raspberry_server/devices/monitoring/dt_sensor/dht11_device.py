from uuid import UUID, uuid4

from logging import getLogger
from devices.utils import Singleton, Error
import adafruit_dht
import board

logger = getLogger()

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
        self.instance = adafruit_dht.DHT11(board.D16)

    def read(self) -> tuple[Error, float, float]:
        """Read data from dht11 sensor."""
        logger.info("Try to read instance")
        try:
            temperature = self.instance.temperature
            humidity = self.instance.humidity
            return (Error.OK, temperature, humidity)
        except (RuntimeError, ValueError, TypeError):
            return (Error.ERR_READ, 0.0, 0.0)
