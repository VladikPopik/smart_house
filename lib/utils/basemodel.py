import typing as ty
import json
from pydantic import BaseModel, model_validator


class Base(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def model_validate_json(
        cls,
        json_data: str | bytes | bytearray,
        *,
        strict: bool | None = None,
        context: ty.Any | None = None
    ) -> ty.Self | ty.ByteString:
        if isinstance(json_data, str) or isinstance(json_data, bytes):
            return cls(**json.loads(json_data))
        return json_data
