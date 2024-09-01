from .config_parser import Config

config: Config = Config() # type: ignore
config.construct(
    "smart_house/conf/manager.json"
)
config.parse_config()

__all__ = ["config"]
