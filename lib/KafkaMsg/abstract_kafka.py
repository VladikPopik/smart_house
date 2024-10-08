import typing as ty

from abc import ABC, abstractmethod

from kafka import Topic

class AbstractConsumer[T](ABC):
    @abstractmethod
    def recieve(self, topic: str) -> dict[str, ty.Any]:
        """Recieve message via kafka."""
        ...

    @abstractmethod
    def subscribe(self, topics: tuple[str | None]) -> tuple[str | None]:
        """Subscribe to topics in kafka."""
        ...

    @abstractmethod
    def unsubscribe() -> None:
        """Unsubscribe from all topics."""
        ...

    @abstractmethod
    def _read_data(self, msg: T) -> T:
        """Cast data for receive method."""
        ...
