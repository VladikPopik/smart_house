import typing as ty


class Singleton(type):
    _instances: ty.ClassVar[dict[ty.Any, ty.Any]] = {}

    def __call__(
        cls, *args: ty.Tuple[ty.Any], **kwargs: dict[dict, dict]
    ) -> None:
        """Singleton class call."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(
                *args, **kwargs
            )
        return cls._instances[cls]
