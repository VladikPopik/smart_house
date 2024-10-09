import typing as ty
from sqlalchemy import insert, select # delete, update
from .table import user_table, login_table
from lib.db import db_instance

async def create_user(user_info: ty.Dict[str, ty.Any]) -> None:
    async with db_instance.session() as session:
        session.execute(insert(user_table).values(**user_info))
        session.commit()

async def get_user(user_login: str) -> ty.Dict[str, ty.Any]:
    async with db_instance.session() as session:
        user: ty.Dict[ty.Any, ty.Any] = session.execute(
            select(user_table).
            where(
                user_table.c.user_login==user_login
            )
        ).first()
        session.commit()

        return user

async def register_user(login_info: ty.Dict[ty.Any, ty.Any]) -> None:
    async with db_instance.session() as session:
        session.execute(insert(login_table).values(**login_info))
        session.commit()
