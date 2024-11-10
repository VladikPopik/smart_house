import uuid

from sqlalchemy import CHAR, FLOAT, TIMESTAMP, Column, MetaData, String, Table

budget_table = Table(
    "budget",
    MetaData(),
    Column("id", CHAR(32), primary_key=True, default=uuid.uuid4()),
    Column("ts_from", TIMESTAMP, primary_key=True, nullable=False),
    Column("ts_to", TIMESTAMP, nullable=False),
    Column("plan_money", FLOAT, nullable=False),
    Column("budget_type", String, nullable=False),
)
