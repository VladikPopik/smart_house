import typing as ty

import json

from collections.abc import AsyncGenerator
from .abstract_kafka import AbstractConsumer

from contextlib import asynccontextmanager

from kafka import KafkaConsumer

class BaseConsumer[T, R](AbstractConsumer[T, R]):
    """Base consumer realization."""
    def __init__(self,
    *topics: tuple[ty.Any, ...],
    **configs: dict[str, ty.Any]
    ) -> None:
        self._consumer = KafkaConsumer(
            *topics,
            **configs
        )

    def recieve(self, _topic: str) -> dict[str, R]:
        """Recieve message via kafka."""
        try:
            msg: T = next(self._consumer)
            msg = self._cast_data(msg)
            return msg
        except Exception as e:
            raise e

    def subscribe(self, topics: tuple[str | None]) -> tuple[str | None]:
        """Subscribe to topics in kafka."""
        self._consumer.subscribe(topics)
        return topics

    def _cast_data(self, msg: T) -> R:
        """Cast data for receive method."""
        return msg

    @asynccontextmanager
    async def get_consumer(self) -> AsyncGenerator[ty.Self | None, None]:
        """Base consumer async context manager."""
        consumer = self._consumer
        try:
            yield consumer if consumer.bootstrap_connected() else None
        except Exception as e:
            consumer.close()
            consumer.unsubscribe()
            raise e
        finally:
            consumer.commit()

json_type_alias: ty.TypeAlias = dict[str, ty.Any]
json_return_type_alias: ty.TypeAlias = dict[str, ty.Any] | list[ty.Any]

class JSONConsumer[
    json_type_alias,
    json_return_type_alias
](
    BaseConsumer[
        json_type_alias,
        json_return_type_alias
    ]
):
    @ty.override
    def _cast_data(self, msg: json_type_alias) -> json_return_type_alias:
        try:
            return json.load(msg)
        except json.JSONDecodeError as e:
            print(f"{e}")
            raise e
        

class StrConsumer[
    bytes,
    str
](
    BaseConsumer[
        bytes,
        str
    ]
):
    @ty.override
    def _cast_data(self, msg: bytes) -> str:
        try:
            return msg.decode("utf-8")
        except UnicodeDecodeError as e:
            print(f"{e}")
            raise e