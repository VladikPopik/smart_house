from .db_instance import DBInstance

db_instance: DBInstance = DBInstance()  # pyright: ignore[reportAssignmentType]

__all__ = ["DBInstance"]
