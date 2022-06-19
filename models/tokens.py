import sqlalchemy
from sqlalchemy import Table, Column, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID

from models.users import users_table

metadata = sqlalchemy.MetaData()

tokens_table = Table(
    "tokens",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "token",
        UUID(as_uuid=False),
        server_default=sqlalchemy.text("uuid_generate_v4()"),
        unique=True,
        nullable=False,
        index=True,
    ),
    Column("expires", DateTime()),
    Column("user_id", sqlalchemy.ForeignKey(users_table.c.id)),
)
