import json
import typing as ty
from pathlib import Path

from .config import JWT, SERVICE, SQL_CONNECTION, SSL
from lib.utils import Singleton

class Config(metaclass=Singleton):
    config_file: str | Path = ""

    def construct(self, config_file: str | Path | None = None) -> None:
        if config_file:
            self.config_file = config_file

    def parse_config(self) -> None:
        with open(self.config_file, "r") as cfg:
            data = json.load(cfg)
            
        self.ssl_conn: SSL = SSL(**data.get("SSL"))
        self.sql_conn = SQL_CONNECTION(**data.get("SQL"))
        self.service = SERVICE(**data.get("SERVICE"))
        self.JWT: JWT = JWT(**data.get("JWT"))

    @property
    def SSL_ENABLED(self) -> bool:
        return self.ssl_conn.PROTOCOL == "https"
