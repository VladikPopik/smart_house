from uuid import UUID, uuid4

import dht11  # pyright: ignore[reportMissingTypeStubs]

type DhtReturnType = dht11.DHT11Result | None


class DhtSensor[T]:
    """Class to handle DHT11 sensor working."""

    def __init__(self, pin: int, name: str) -> None:
        self.name = name
        self.uuid: UUID = uuid4()
        self.pin = pin
        self.instance = dht11.DHT11(pin=pin)

    def read(self) -> DhtReturnType:
        """Read data from dht11 sensor."""
        result = self.instance.read()

        if result.is_valid():
            return result

        error = f"Cannot read from pin={self.pin} due to code number {result.error_code}"
        raise ValueError(error)
