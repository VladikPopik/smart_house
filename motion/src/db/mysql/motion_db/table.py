import uuid

from sqlalchemy import CHAR, FLOAT, TIMESTAMP, Column, MetaData, String, Table

monitoring_table = Table(
    "motion",
    MetaData(),
    Column("id", CHAR(32), primary_key=True, default=uuid.uuid4()),
    Column("inserted_at", TIMESTAMP, primary_key=True, nullable=False)
)