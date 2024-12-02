from contextlib import contextmanager

import sqlalchemy as sa

from library.conf import config
from library.utils import Singleton


class DBInstance(metaclass=Singleton):
    def __init__(self) -> None:
        url = sa.URL.create(
            # config.sql_conn.engine,
            # username=config.sql_conn.user,
            # password=config.sql_conn.password,
            # host=config.sql_conn.host,
            # database=config.sql_conn.db,
            # port=config.sql_conn.port,
            drivername="mysql+pymysql",
            username="root",
            password="admin",
            host="0.0.0.0",
            database="test",
            port=3306
        )
        self.engine: sa.Engine = sa.create_engine(url=url)

    @contextmanager
    def session(self):  # noqa: ANN201
        """Context manager for db connection."""
        conn = self.engine.connect()
        try:
            yield conn
        except Exception as e:  # noqa: E722
            # TODO <me>: Create logger system
            conn.rollback()
            print(e, "******************************")
            # raise Exception("Cannot connect to db")
        finally:
            conn.commit()
            conn.close()
