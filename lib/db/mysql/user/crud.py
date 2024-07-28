import typing as ty
from sqlalchemy import insert, select# delete, update
from .table import user_table
from lib.db.db_instance import dbInstance

async def create_user(user_info: ty.Dict[str, ty.Any]) -> None:
    with dbInstance().session() as session:
        session.execute(insert(user_table).values(**user_info))
        session.commit()

async def get_user(user_login: str) -> ty.Dict[str, ty.Any]:
    with dbInstance().session() as session:
        user: ty.NamedTuple[str, ty.Any] = session.execute(
            select(user_table).
            where(
                user_table.c.user_login==user_login
            )
        ).first()
        session.commit()

    return user
