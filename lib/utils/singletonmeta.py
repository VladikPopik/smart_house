import typing as ty

class Singleton(type):
    _instances: ty.Dict[ty.Any, ty.Any] = {}
    def __call__(cls,
        *args: ty.Tuple[ty.Any],
        **kwargs: ty.Dict[ty.Any, ty.Any]
    )-> None:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
