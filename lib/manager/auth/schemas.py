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
        context: ty.Any | None = None) -> ty.Self:
        if (
            isinstance(json_data, str) or
            isinstance(json_data, bytes)
        ):
            return cls(**json.loads(json_data))
        return json_data

class CreateUser(Base):
    user_name: str = "Default"
    user_login: str
    user_email: str
    tg_login: str
    password: str
    is_superuser: bool = False


class RegisterUser(Base):
    user_login: str
    password: str

class GetToken(Base):
    access_token: str
    token_type: str = "bearer"

class LoginUser(Base):
    user_login: str
    password: str
