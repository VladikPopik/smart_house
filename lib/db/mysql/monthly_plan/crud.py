import datetime
import typing as ty
import uuid
from collections.abc import Sequence

from sqlalchemy import RowMapping, delete, insert, select, update

from lib.db import db_instance

from .table import budget_table


async def create_budget(
    ts_from: datetime.time,
    ts_to: datetime.time,
    plan_money: float,
    budget_type: str,
) -> None:
    """CRUD to create budget."""
    with db_instance.session() as session:
        session.execute(
            insert(budget_table).values(
                id=uuid.uuid4(),
                ts_from=ts_from,
                ts_to=ts_to,
                plan_money=plan_money,
                budget_type=budget_type,
            )
        )


async def read_budget(uuid: uuid.UUID) -> RowMapping | None:
    """Read all budgets from db."""
    with db_instance.session() as session:
        return (
            session.execute(
                select(budget_table).where(budget_table.c.id == uuid)
            )
            .mappings()
            .fetchone()
        )


async def read_budget_by_start_time(ts_from: float) -> RowMapping | None:
    """Read one budget by time."""
    with db_instance.session() as session:
        return (
            session.execute(
                select(budget_table).where(budget_table.c.ts_from == ts_from)
            )
            .mappings()
            .fetchone()
        )


async def delete_budget(uuid: uuid.UUID) -> None:
    """CRUD delete for budget."""
    with db_instance.session() as session:
        session.execute(delete(budget_table).where(budget_table.c.id == uuid))


async def update_budget(
    uuid: uuid.UUID, **budget_info: ty.Dict[str, ty.Any]
) -> RowMapping | None:
    """CRUD update for budget."""
    with db_instance.session() as session:
        return session.execute(
            update(budget_table)
            .where(budget_table.c.id == uuid)
            .values(**budget_info)
        ).fetchone()  # pyright: ignore[reportReturnType]


async def get_budgets() -> Sequence[RowMapping]:
    """CRUD read for budget."""
    with db_instance.session() as session:
        return session.execute(select(budget_table)).mappings().fetchall()
