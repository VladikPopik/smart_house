import typing as ty
from contextlib import asynccontextmanager
import sqlalchemy as sa

from lib.conf import config
from lib.utils import Singleton

class dbInstance(metaclass=Singleton):
    def __init__(self) -> None:
        url = sa.URL.create(
            config.sql_conn.engine,
            username=config.sql_conn.user,
            password=config.sql_conn.password,
            host=config.sql_conn.host,
            database=config.sql_conn.db,
            port=config.sql_conn.port
        )
        self.engine: sa.Engine = sa.create_engine(url=url)

    @asynccontextmanager
    def session(self) -> ty.Any:  # ty.Generator[sa.Connection | None | None]
        conn = self.engine.connect()
        try:
            yield conn
            conn.commit()
        except:
            raise Exception("Cannot connect to bd")
        finally:
            conn.rollback()
            conn.close()
