import uuid

from sqlalchemy import CHAR, FLOAT, TIMESTAMP, Column, MetaData, String, Table

monitoring_table = Table(
    "monitoring",
    MetaData(),
    Column("time", TIMESTAMP, primary_key=True),
    Column("temperature", FLOAT),
    Column("humidity", FLOAT)
)