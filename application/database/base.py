import asyncpgsa
from .db import tokens
from sqlalchemy import (
    select, insert, delete, text, asc
)


async def on_start(app):
    """
    When the application starts it will configure the database with
    options from the 'database_config' which are places at config.yaml.
    """
    config = app['config']
    app['db'] = await asyncpgsa.create_pool(**config['database_config'])


async def insert_token_into_db(app, token):
    async with app['db'].acquire() as conn:
        query = insert(tokens).values(
            token=token
        )
        await conn.fetchrow(query)


# TODO think how to optimize
async def delete_token_from_db(app, token):
    """Delete a token from database.

    Keywords arguments:
    app -- the application
    token -- the deleting token

    """
    async with app['db'].acquire() as conn:
        # Looking for passed token, specifically its id.
        search_token_id = await conn.fetch(select([tokens.c.id]).where(tokens.c.token == token))
        # Receive the if of the first token in the table.
        first_token_id = await conn.fetch(select([tokens.c.id]).order_by(asc(tokens.c.id)).limit(1))
        # If they are coincide i.e. the passed token is first in the table then delete it from the table.
        #
        if search_token_id == first_token_id:
            query = delete(tokens).where(tokens.c.id == search_token_id[0]['id']).returning(tokens.c.token)
            result = await conn.fetch(query)
            return True, result[0]['token']
        elif search_token_id:
            return False, True
        else:
            return False, False


async def on_shutdown(app):
    """
    When the application ends its work it will close the connection with database
    """
    async with app['db'].acquire() as conn:
        query = delete(tokens)
        await conn.fetchrow(query)
        await conn.execute("ALTER SEQUENCE tokens_id_seq RESTART ")
    await app['db'].close()


