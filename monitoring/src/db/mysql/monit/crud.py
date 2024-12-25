import datetime
import typing as ty
import uuid
from collections.abc import Sequence
from logging import getLogger

from sqlalchemy import RowMapping, delete, insert, select, update, func

from src.db import db_instance
from .table import monitoring_table

log = getLogger()


async def create_record(
    time,
    temperature,
    humidity
) -> None:
    with db_instance.session() as session:
        try:
            # Преобразуем метку времени в формат DATETIME
            time_as_datetime = datetime.datetime.fromtimestamp(float(time))
            
            session.execute(
                insert(monitoring_table).values({
                    "time": time_as_datetime,
                    "temperature": temperature,
                    "humidity": humidity
                })
            )
            log.info("Запись успешно произведена!")
        except Exception as e:
            log.error(f"Ошибка при вставке записи: {e}")

async def get_records_batch(batch_size: int, current_offset: int) -> tuple[list[dict], int]:
    """
    Получение записей из таблицы monitoring, проверяя накопление `batch_size` записей.
    Динамически обновляет оффсет после каждой обработки данных.

    :param batch_size: Размер партии записей для обработки.
    :param current_offset: Текущий оффсет для выборки.
    :return: Кортеж (список записей, обновленный оффсет).
    """
    with db_instance.session() as session:  # Предполагается, что db_instance предоставляет AsyncSession
        try:
            # Подсчитываем общее количество записей в таблице
            total_query = select(func.count()).select_from(monitoring_table)
            total_records = (session.execute(total_query)).scalar()
            
            # Ждем, пока в таблице накопится достаточно записей
            if total_records < current_offset + batch_size:
                log.info(f"Недостаточно записей для обработки. Доступно: {total_records}, нужно: {current_offset + batch_size}.")
                return [], current_offset

            # Получаем записи с текущим оффсетом
            query = select(monitoring_table).offset(current_offset).limit(batch_size)
            result = session.execute(query)
            
            # Преобразуем результат в список словарей
            records = [
                {
                    "time": row.time,
                    "temperature": row.temperature,
                    "humidity": row.humidity
                }
                for row in result.fetchall()
            ]
            log.info(current_offset + len(records))
            return records, current_offset + len(records)
        except Exception as e:
            log.error(f"Ошибка при получении записей: {e}")
            return [], current_offset