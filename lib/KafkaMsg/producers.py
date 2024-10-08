import typing as ty

import json

from .abstract_kafka import AbstractProducer
from kafka import KafkaProducer

from collections.abc import AsyncGenerator

class BaseProducer[T, R](AbstractProducer[T, R]):
    def __init__(self, **configs: dict[str, ty.Any]) -> None:
        self._producer = KafkaProducer(**configs)

    def send(self, topic: str, value: T, key: str) -> None:
        """Method to send message via kafka."""
        try:
            value = self._convert_data(value)
            self._producer.send(topic, value, key)
        except Exception as e:
            print(f"{e}")
            raise e

    def close(self, timeout: int) -> bool:
        """Close producer."""
        self._producer.close(timeout)

    def _cast_data(self, data: T) -> R:
        return data

    async def get_producer(self) -> AsyncGenerator[ty.Self, None, None]:
        """Context manager to get consumer."""
        producer = self._producer
        try:
            yield producer if producer.bootstrap_connected() else None
        except Exception as e:
            print(f"{e}")
            raise e

json_type_alias: ty.TypeAlias = dict[str, ty.Any] | list[ty.Any]
json_return_type_alias: ty.TypeAlias = dict[str, ty.Any]

class JSONProducer(
    BaseProducer[
        json_type_alias,
        json_return_type_alias
    ]
):
    @ty.override
    def _cast_data(self, data: json_type_alias) -> json_return_type_alias:
        try:
            return json.dump(data)
        except json.JSONDecodeError as e:
            print(f"{e}")
            raise e
        

class StrProducer(
    BaseProducer[
        str, bytes
    ]
):
    @ty.override
    def _cast_data(self, data: str) -> bytes:
        try:
            return data.encode()
        except Exception as e:
            print(f"{e}")
            raise e