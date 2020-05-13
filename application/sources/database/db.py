"""In this module defined some settings for sqlalchemy, specifically for database.
You may familiarize with documentation https://docs.sqlalchemy.org/en/13/dialects/postgresql.html
"""

from sqlalchemy import (
    Table, Integer, VARCHAR, MetaData, Column
)

__all__ = ('tokens',)

# Creating a collection of table objects and their associated schema constructs.
meta = MetaData()

# Creating table with 2 columns: 'id' and 'token'
tokens = Table(
    'tokens', meta,
    Column('id', Integer, primary_key=True),
    Column('token', VARCHAR(3), nullable=True),
)
