from .config_parser import Config

config: Config = Config()  # type: ignore
config.construct("/home/makza/smart_house/smart_house/monitoring/config/manager.json")
config.parse_config()

__all__ = ["config"]
