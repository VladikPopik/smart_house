import typing as ty
import dht11  # pyright: ignore[reportMissingTypeStubs]


class DhtSensor[T]:
    """Class to handle DHT11 sensor working."""

    def __init__(self, pin: int) -> None:
        self.instance = dht11.DHT11(pin=pin)

    def read(self) -> dht11.DHT11Result | T:
        """Read data from dht11 sensor."""
        result = self.instance.read()

        if result.is_valid():
            return result

        return ty.cast(
            T, result.error_code
        )  # pyright: ignore[reportUnknownMemberType]
