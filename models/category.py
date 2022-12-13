from sqlalchemy import Column, Identity, Table
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

category = Table(
    "categories",
    meta,
    Column("id", Integer,autoincrement = True, primary_key=True),
    Column(
        "name",
        String(255),
    ),
    Column("descriptions", String(2000)),
)

meta.create_all(engine)