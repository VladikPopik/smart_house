import datetime
import typing as ty
import uuid

from sqlalchemy import delete, insert, select, update

from lib.db.db_instance import dbInstance

from .table import budget_table


async def create_budget(
    ts_from: datetime.time,
    ts_to: datetime.time,
    plan_money: float,
    budget_type: str,
) -> None:
    with dbInstance().session() as session:
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
    with dbInstance().session() as session:
        budget = session.execute(
            select(budget_table).where(budget_table.c.id == uuid)
        )
        session.commit()

    return budget


async def read_budget_by_start_time(ts_from) -> list[ty.Any]:
    with dbInstance().session() as session:
        budgets = session.execute(
            select(budget_table).where(budget_table.c.ts_from == ts_from)
        )
        session.commit()

    return list(budgets)


async def delete_budget(uuid: uuid.UUID) -> None:
    with dbInstance().session() as session:
        session.execute(delete(budget_table).where(budget_table.c.id == uuid))
        session.commit()

    return


async def update_budget(uuid, **budget_info: ty.Dict[str, ty.Any]) -> uuid.UUID:
    with dbInstance().session() as session:
        uuid = session.execute(
            update(budget_table)
            .where(budget_table.c.id == uuid)
            .values(**budget_info)
        )
        session.commit()

    return uuid
