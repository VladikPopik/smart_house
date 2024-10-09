import datetime
import typing as ty
import uuid

from sqlalchemy import delete, insert, select, update

from lib.db import db_instance

from .table import budget_table


async def create_budget(
    ts_from: datetime.time,
    ts_to: datetime.time,
    plan_money: float,
    budget_type: str,
) -> None:
    async with db_instance.session() as session:
        session.execute(
            insert(budget_table).values(
                id=uuid.uuid4(),
                ts_from=ts_from,
                ts_to=ts_to,
                plan_money=plan_money,
                budget_type=budget_type,
            )
        )
        session.commit()
    return


async def read_budget(uuid: uuid.UUID) -> tuple[ty.Any]:
    async with db_instance.session() as session:
        budget = session.execute(
            select(budget_table).where(budget_table.c.id == uuid)
        )
        session.commit()

    return budget


async def read_budget_by_start_time(ts_from) -> list[ty.Any]:
    async with db_instance.session() as session:
        budgets = session.execute(
            select(budget_table).where(budget_table.c.ts_from == ts_from)
        )
        session.commit()

    return list(budgets)


async def delete_budget(uuid: uuid.UUID) -> None:
    async with db_instance.session() as session:
        session.execute(delete(budget_table).where(budget_table.c.id == uuid))
        session.commit()

    return


async def update_budget(uuid, **budget_info: ty.Dict[str, ty.Any]) -> uuid.UUID:
    async with db_instance.session() as session:
        uuid = session.execute(
            update(budget_table)
            .where(budget_table.c.id == uuid)
            .values(**budget_info)
        )
        session.commit()

    return uuid

async def get_budgets() -> ty.Any:
    async with db_instance.ession() as session:
        data = session.execute(
            select(budget_table)
        )
    return data