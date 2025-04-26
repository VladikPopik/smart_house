import datetime
import typing as ty
import pickle
import numpy as np
import uuid
from collections.abc import Sequence
from logging import getLogger

from sqlalchemy import (
    RowMapping,
    delete,
    insert,
    select,
    update,
    func,
    desc
)

from src.db import db_instance
from .table import monitoring_table

log = getLogger()

OFFSET = 0 


async def create_record(
    payload: ty.Dict,
) -> None:
    with db_instance.session() as session:
        session.execute(
            insert(monitoring_table).values(
                time = payload['time'],
                temperature = payload['temperature'],
                humidity = payload['humidity']
            )
        )
        # log.info("Запись успешно произведена!")      

async def fetch_last_60_temps_for_prediction():
    with db_instance.session() as session:
        # current_offset = OFFSET

        temperatures = session.execute(
            select(monitoring_table.c.temperature)
            .limit(60)
        ).scalars().all()

        if len(temperatures) < 60:
            log.info("Недостаточно данных с оффсета")
            return
    
        # temps_array = np.array(temperatures)

        # OFFSET += 15

        return temperatures



async def predict_next_temperatures(temepratures: tuple):

    with open('svr_temperature_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)

    X_input = temepratures.reshape((1, -1))

   
    predicted_values = loaded_model.predict(X_input)[0]

    return predicted_values

    # log.info(f"Предсказанные значения температуры: {predicted_values}")
    # log.info(f"Текущее смещение (last_offset): {OFFSET}")
