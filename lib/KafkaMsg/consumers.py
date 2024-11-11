import json
import typing as ty
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from aiokafka import AIOKafkaConsumer

from lib.conf import Config, config

from .abstract_kafka import AbstractConsumer


class BaseConsumer[T, R](AbstractConsumer[T, R]):
    """Base consumer realization."""

    def __init__(
        self, *topics: tuple[ty.Any, ...], _configs: Config = config
    ) -> None:
        self._consumer = AIOKafkaConsumer(
            *topics, **_configs.Kafka.model_dump()
        )

    async def recieve(self, _topic: str | None = None) -> dict[str, R]:
        """Recieve message via kafka."""
        data: dict[str, R] = {}
        consumer = self._consumer
        try:
            await self.subscribe()
            msg = await consumer.getone()
            data[msg.key] = self._cast_data(
                msg.value
            )  # pyright: ignore[reportArgumentType]
        except Exception as e:
            print(e)
        return data

    async def subscribe(self) -> None:
        """Subscribe to topics in kafka."""
        await self._consumer.start()  # pyright: ignore[reportGeneralTypeIssues]

    def _cast_data(self, msg: T) -> R:
        """Cast data for receive method."""
        return ty.cast(R, msg)

    @asynccontextmanager
    async def get_consumer(self) -> AsyncGenerator[ty.Self | None, None]:
        """Base consumer async context manager."""
        try:
            yield self
        except Exception as e:
            print(e)
        finally:
            await self._consumer.commit()
            await self._consumer.stop()


type json_type_alias = dict[str, ty.Any]
type json_return_type_alias = dict[str, ty.Any] | list[ty.Any]


class JSONConsumer[json_type_alias, json_return_type_alias](
    BaseConsumer[json_type_alias, json_return_type_alias]
):
    @ty.override
    def _cast_data(self, msg: json_type_alias) -> json_return_type_alias:
        try:
            return json.load(msg.decode())  # pyright: ignore[reportAttributeAccessIssue, reportArgumentType]
        except json.JSONDecodeError as e:
            print(f"{e}")
            raise e


class StrConsumer[bytes, str](BaseConsumer[bytes, str]):
    @ty.override
    def _cast_data(self, msg: bytes) -> str:
        data: str = ""  # pyright: ignore[reportAssignmentType]
        try:
            data = msg.decode(
                "utf-8"
            )  # pyright: ignore[reportAttributeAccessIssue]
        except UnicodeDecodeError as e:
            print(f"{e}")
        return data
