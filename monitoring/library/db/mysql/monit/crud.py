import datetime
import typing as ty
import uuid
from collections.abc import Sequence

from sqlalchemy import RowMapping, delete, insert, select, update

from library.db import db_instance
from .table import monitoring_table


async def create_record(
    inserted_at: datetime.time,
) -> None:
    with db_instance.session() as session:
        session.execute(
            insert(monitoring_table).values(
                id=uuid.uuid4(),
                inserted_at=inserted_at
            )
        )
        print("Запись успешно произведена!")      
