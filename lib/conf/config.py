import typing as ty
import json
from pydantic import BaseModel, model_validator


class Base(BaseModel): 
    @model_validator(mode="before")
    @classmethod
    def model_validate_json(
        cls,
        json_data: str | bytes | bytearray,
        *, strict: bool | None = None,
        context: ty.Any | None = None) -> ty.Self | ty.ByteString:
        if (
            isinstance(json_data, str) or
            isinstance(json_data, bytes)
        ):
            return cls(**json.loads(json_data))
        return json_data


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
