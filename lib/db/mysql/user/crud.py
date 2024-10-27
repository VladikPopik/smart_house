import typing as ty
from sqlalchemy import insert, select  # delete, update
from .table import user_table, login_table
from lib.db import db_instance


async def create_user(user_info: ty.Dict[str, ty.Any]) -> None:
    """CRUD create user."""
    with db_instance.session() as session:
        session.execute(insert(user_table).values(**user_info))


async def get_user(user_login: str) -> dict[str, ty.Any]:
    """CRUD get user."""
    with db_instance.session() as session:
        user: ty.Dict[ty.Any, ty.Any] = session.execute(
            select(user_table).where(user_table.c.user_login==user_login)
        ).first()

        return user


async def register_user(login_info: dict[ty.Any, ty.Any]) -> None:
    """CRUD register user."""
    with db_instance.session() as session:
        session.execute(insert(login_table).values(**login_info))
