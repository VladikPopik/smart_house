from sqlalchemy import Boolean, Column, MetaData, String, Table, ForeignKey

user_table = Table(
    "user",
    MetaData(),
    Column("user_login", String(100), primary_key=True),
    Column("user_name", String(100)),
    Column("user_email", String(100)),
    Column("tg_login", String(100)),
    Column("is_superuser", Boolean, default=False),
)


login_table = Table(
    "login",
    MetaData(),
    Column(
        "user_login",
        String(100),
        ForeignKey("users.user_login"),
        nullable=False,
    ),
    Column("user_password", String(100)),
)
