import datetime
import typing as ty
import uuid
from collections.abc import Sequence
from logging import getLogger

from sqlalchemy import RowMapping, delete, insert, select, update

from src.db import db_instance
from .table import monitoring_table

log = getLogger()


async def create_record(
    payload: ty.Dict,
) -> None:
    with db_instance.session() as session:
        session.execute(
            insert(monitoring_table).values(
                time = payload['time'],
                temperature = payload['temperature'],
                humidity = payload['humidity']
            )
        )
        log.info("Запись успешно произведена!")      
