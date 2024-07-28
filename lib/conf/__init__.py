from .config_parser import Config

config: Config | None = Config()
config.construct(
    "/home/vladikpopik/my_projects/smart_house/backend/smart_house/conf/manager.json"
)
config.parse_config()

__all__ = ["config"]
