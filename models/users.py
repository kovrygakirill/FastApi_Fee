from sqlalchemy import Table, Column, Boolean, Integer, String
import sqlalchemy

metadata = sqlalchemy.MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(40), unique=True, index=True),
    Column("name", String(100)),
    Column("hashed_password", String()),
    Column(
        "is_active",
        Boolean(),
        server_default=sqlalchemy.sql.expression.true(),
        nullable=False,
    ),
)
