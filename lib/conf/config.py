import typing as ty

from pydantic import BaseModel


class Base(BaseModel): ...


class SSL(Base):
    PROTOCOL: ty.Literal["http", "https"]
    SSL_KEY: str
    SSL_CERT: str


class SQL_CONNECTION(Base):
    CONNECTION_STRING: str


class SERVICE(Base):
    host: str
    port: int
    log_level: str
