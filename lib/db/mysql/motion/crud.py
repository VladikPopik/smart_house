import typing as ty
import uuid

from sqlalchemy import insert, select

from lib.db import db_instance
from .table import alerts_table


async def create_alert(**alert_params: dict[str, ty.Any]) -> None:
    """Function to create alert in db."""
    with db_instance.session() as session:
        session.execute(
            insert(alerts_table).values(
                **alert_params
            )
        )

async def read_alert(uuid: uuid.UUID) -> dict[str, ty.Any]:
    """Function to read alert by uuid from db."""
    with db_instance.session() as session:
        res = session.execute(
            select(alerts_table).where(
                alerts_table.c.uuid==uuid
            )
        )
    return res
