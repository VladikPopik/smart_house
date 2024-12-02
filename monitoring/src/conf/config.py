import typing as ty

from src.utils.basemodel import Base


class SSL(Base):
    PROTOCOL: ty.Literal["http", "https"]
    SSL_KEY: str
    SSL_CERT: str


class SQL_CONNECTION(Base):
    engine: str
    user: str
    password: str
    host: str
    port: int
    db: str


class SERVICE(Base):
    host: str
    port: int
    log_level: str


class JWT(Base):
    SECRET_KEY: str = "my_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


class Origins(Base):
    host: str = "localhost"
    port: int = 5173


class Kafka(Base):
    bootstrap_servers: str = "kafka:9092"
