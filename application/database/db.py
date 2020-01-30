from sqlalchemy import (
    Table, Text, Integer, VARCHAR, MetaData, Column
)

meta = MetaData()

tokens = Table(
    'tokens', meta,
    Column('id', Integer, primary_key=True),
    Column('token', VARCHAR(4), nullable=True)
)
