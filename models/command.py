from sqlalchemy import Column, Identity, Table,ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

commands = Table(
    "Commands",
    meta,
    Column("id", Integer,autoincrement = True, primary_key=True),
    Column(
        "name",
        String(255),
    ),
    Column("command", String(2000)),
    Column("categoryId", Integer),
)

meta.create_all(engine)