from sqlalchemy import CHAR, TIMESTAMP, Column, MetaData, Table

alerts_table = Table(
    "alerts",
    MetaData(),
    Column("uuid", CHAR(64), primary_key=True),
    Column("date", TIMESTAMP, nullable=False),
    Column("status", CHAR(2)),
)
