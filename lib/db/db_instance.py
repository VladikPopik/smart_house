import typing as ty
from contextlib import contextmanager

import sqlalchemy as sa

from lib.conf import config
from lib.utils import Singleton


class dbInstance(metaclass=Singleton):
    def __init__(self) -> None:
        self.engine: sa.Engine = sa.create_engine(
            config.sql_conn.CONNECTION_STRING
        )

    @contextmanager
    def session(self) -> ty.Generator:
        conn = self.engine.connect()
        try:
            yield conn
        except:
            conn.close()

    def close_connection(self) -> None:
        self.engine.close()
