import typing as ty

from pydantic import BaseModel
from starlette.routing import Host


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


class JWT(Base):
    SECRET_KEY: str = "my_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
