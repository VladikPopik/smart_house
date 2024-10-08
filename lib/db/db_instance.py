import typing as ty
from contextlib import contextmanager
import sqlalchemy as sa

from lib.conf import config
from lib.utils import Singleton

from collections.abc import Generator

class DBInstance(metaclass=Singleton):
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

    @contextmanager
    def session(self) -> Generator["sa.Connection"]:  # ty.Generator[sa.Connection | None | None]
        conn = self.engine.connect()
        try:
            yield conn
        except Exception as e:
            print(f"{e}")
        finally:
            conn.close()
