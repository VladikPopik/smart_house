from enum import IntEnum
from .singletonmeta import Singleton

class Error(IntEnum):
    OK = 0
    ERR_READ = 1
    ERR_ETC = 2

__all__ = ["Singleton", "Error"]
