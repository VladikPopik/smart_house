from enum import IntEnum
from .singletonmeta import Singleton

class Error(IntEnum):
    OK = 0
    ERR_READ = 1
    ERR_ETC = 2

def convert_error(service: str, err: Error) -> str:
    match err:
        case Error.OK:
            return f"Подсистема {service} стабильна, ошибок нет"
        case Error.ERR_READ:
            return f"Подсистема {service} не смогла считать данные с датчика"
        case Error.ERR_ETC:
            return f"Подсистема {service} не отвечает, обратитесь к администратору"
        case _:
            return f"Подсистема {service} не отвечает, обратитесь к администратору"


__all__ = ["Singleton", "Error", "convert_error"]
