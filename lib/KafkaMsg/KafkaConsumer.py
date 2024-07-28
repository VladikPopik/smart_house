import typing as ty

from kafka import KafkaConsumer


class KafkaConsumerFactory:
    @classmethod
    def create_consumer(cls, *args: ty.Any, **kwargs: ty.Any) -> KafkaConsumer:
        cls.consumer = KafkaConsumer(
            *args, **kwargs
        )

    @classmethod
    def send_msg(cls, msg: str | bytes | dict[ty.Any, ty.Any]):
        ...
