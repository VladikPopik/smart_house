import json
from pathlib import Path

from .config import SERVICE, SQL_CONNECTION, SSL


class Config:
    config_file: str | Path = ""

    @classmethod
    def construct(cls, config_file: str | Path | None = None) -> None:
        if config_file:
            cls.config_file = config_file

    @classmethod
    def parse_config(cls) -> None:
        with open(cls.config_file, "r") as cfg:
            data = json.load(cfg)
        cls.ssl_conn: SSL = SSL(**data["SSL"])
        cls.sql_conn = SQL_CONNECTION(**data["SQL"])
        cls.service = SERVICE(**data["SERVICE"])

    @classmethod
    def SSL_ENABLED(cls) -> bool:
        return cls.ssl_conn.PROTOCOL == "https"
