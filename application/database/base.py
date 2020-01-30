import asyncpgsa
from sqlalchemy import select, insert
from .db import tokens


async def on_start(app):
    """
    When the application starts it will configure the database with
    options from the 'database_config' which are places at config.yaml.
    """
    config = app['config']
    app['db'] = await asyncpgsa.create_pool(**config['database_config'])


async def on_shutdown(app):
    """
    When the application ends its work it will close the connection with database
    """
    await app['db'].close()


