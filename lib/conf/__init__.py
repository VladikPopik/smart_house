from .config_parser import Config

Config.construct(
    "/home/vladikpopik/my_projects/smart_house/backend/smart_house/conf/manager.json"
)
config: Config = Config
config.parse_config()

__all__ = ["config"]
