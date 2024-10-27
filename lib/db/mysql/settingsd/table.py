from sqlalchemy import Column, MetaData, String, Table, FLOAT, CHAR, INTEGER

settingsd_table = Table(
    "settingsd",
    MetaData(),
    Column("device_name", CHAR(8), primary_key=True),
    Column("device_type", String(100), nullable=False),
    Column(
        "voltage", FLOAT, nullable=False
    ),  # pyright: ignore[reportUnknownArgumentType]
    Column("pin", INTEGER, nullable=False)
)
