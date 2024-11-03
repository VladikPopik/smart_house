import typing as ty

from collections.abc import AsyncGenerator
from abc import ABC, abstractmethod


class AbstractConsumer[T, R](ABC):
    """Absctract Factory for Kafka Consumers."""

    @abstractmethod
    async def recieve(self, _topic: str | None = None) -> dict[str, R]:
        """Recieve message via kafka."""
        ...

    @abstractmethod
    async def subscribe(self, topics: tuple[str | None]) -> tuple[str | None]:
        """Subscribe to topics in kafka."""
        ...

    @abstractmethod
    def _cast_data(self, msg: T) -> R:
        """Cast data for receive method."""
        ...

    @abstractmethod
    async def get_consumer(self) -> AsyncGenerator[ty.Self, None]:
        """Context manager to get consumer."""
        ...


class AbstractProducer[T, R](ABC):
    @abstractmethod
    async def send(self, topic: tuple[str, ...], value: T, key: str) -> None:
        """Method to send message via kafka."""
        ...

    @abstractmethod
    async def close(self, timeout: int) -> bool:
        """Close producer."""
        ...

    @abstractmethod
    def _cast_data(self, data: T) -> R:
        """Cast data into proper type."""
        ...

    @abstractmethod
    async def get_producer(self) -> AsyncGenerator[ty.Self, None]:
        """Context manager to get consumer."""
        ...
