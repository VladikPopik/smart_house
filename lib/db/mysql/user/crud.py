import typing as ty
from sqlalchemy import insert, select, delete, update
from .table import user_table
from lib.db.db_instance import dbInstance

async def create_user(user_info: ty.Dict[str, ty.Any]) -> None:
    with dbInstance().session() as session:
        session.execute(insert(user_table).values(**user_info))
        session.commit()
