import uuid

from sqlalchemy import CHAR, FLOAT, TIMESTAMP, Column, MetaData, String, Table

monitoring_table = Table(
    "monitoring",
    MetaData(),
    Column("time", TIMESTAMP, primary_key=True, nullable=False),
    Column("temperature", FLOAT, nullable=False),
    Column("humidity", FLOAT, nullable=False)
)