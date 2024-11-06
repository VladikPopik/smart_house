import json
from pathlib import Path

from .config import (
    JWT,
    SERVICE,
    SQL_CONNECTION,
    SSL,
    Kafka,
    Origins
)
from lib.utils import Singleton


class Config(metaclass=Singleton):
    config_file: str | Path = ""

    def construct(self, config_file: str | Path | None = None) -> None:
        """Construce config file."""
        if config_file:
            self.config_file = config_file

    def parse_config(self) -> None:
        """Parse config."""
        with Path.open(self.config_file) as cfg: # pyright: ignore[reportArgumentType]
            data = json.load(cfg)

        self.ssl_conn: SSL = SSL(**data.get("SSL"))
        self.sql_conn = SQL_CONNECTION(**data.get("SQL"))
        self.service = SERVICE(**data.get("SERVICE"))
        self.JWT: JWT = JWT(**data.get("JWT"))
        self.Kafka = Kafka(**data.get("Kafka"))
        self.origins = Origins(**data.get("Origins"))

    @property
    def ssl_enabled(self) -> bool:
        """Property to verify about ssl certifications."""
        return self.ssl_conn.PROTOCOL == "https"
