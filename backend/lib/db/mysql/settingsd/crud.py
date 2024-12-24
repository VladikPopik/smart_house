import typing as ty
from collections.abc import Sequence

from sqlalchemy import RowMapping, delete, insert, select, update

from lib.db import db_instance

from .table import settingsd_table


async def create_device[T](params: dict[str, T]) -> None:
    """Create function for device table."""
    with db_instance.session() as session:
        session.execute(insert(settingsd_table).values(**params))


async def read_device_by_type(device_type: str) -> RowMapping | None:
    """Read first device with specified type."""
    with db_instance.session() as session:
        return (
            session.execute(
                select(settingsd_table).where(
                    (settingsd_table.c.device_type == device_type)
                )
            )
            .mappings()
            .fetchone()
        )


async def device_read(device_name: str) -> RowMapping | None:
    """Read function for device table."""
    with db_instance.session() as session:
        return (
            session.execute(
                select(settingsd_table).where(
                    settingsd_table.c.device_name == device_name
                )
            )
            .mappings()
            .fetchone()
        )


async def read_all() -> Sequence[RowMapping]:
    """Read all rows from device table."""
    with db_instance.session() as session:
        result = session.execute(select(settingsd_table))
    return result.mappings().all()


async def device_delete(device_name: str) -> None:
    """Delete row from devices by name."""
    with db_instance.session() as session:
        session.execute(
            delete(settingsd_table).where(
                settingsd_table.c.device_name == device_name
            )
        )


async def device_update[T](device_name: str, params: dict[str, T]) -> str:
    """Update row for device table."""
    with db_instance.session() as session:
        session.execute(
            update(settingsd_table)
            .where(settingsd_table.c.device_name == device_name)
            .values(**params)
        )
    return device_name
