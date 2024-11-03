import typing as ty

import json

from .abstract_kafka import AbstractProducer
from aiokafka import AIOKafkaProducer
from .configs import config_producer


class BaseProducer[T, R](AbstractProducer[T, R]):
    def __init__(self, _configs: dict[str, ty.Any]=config_producer) -> None:
        self._producer = AIOKafkaProducer(**_configs)

    async def send(
        self, topic: str, value: T | None = None, key: str | None = None
    ) -> None:
        """Method to send message via kafka."""
        try:
            value = self._cast_data(value) # pyright: ignore[reportAssignmentType, reportArgumentType]
            await self._producer.send(topic, value, key)
        except Exception as e:
            print(f"{e}")
            raise e

    async def close(self) -> bool:
        """Close producer."""
        await self._producer.stop()
        return True

    def _cast_data(self, data: T) -> R:
        return ty.cast(R, data)

    async def get_producer(self) -> ty.Any:
        """Context manager to get consumer."""
        return self._producer.transaction()


json_type_alias: ty.TypeAlias = dict[str, ty.Any] | list[ty.Any]
json_return_type_alias: ty.TypeAlias = dict[str, ty.Any]


class JSONProducer(BaseProducer[json_type_alias, json_return_type_alias]):
    @ty.override
    def _cast_data(self, data: json_type_alias) -> json_return_type_alias:
        try:
            data = json.dump(data)
        except json.JSONDecodeError as e:
            print(f"{e}")
        return data


class StrProducer(BaseProducer[str, bytes]):
    @ty.override
    def _cast_data(self, data: str) -> bytes:
        try:
            data_: bytes = data.encode()
        except Exception as e:
            print(f"{e}")
        return data_
