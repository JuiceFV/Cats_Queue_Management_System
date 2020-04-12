"""

"""
import asyncpgsa
from .db import tokens
from sqlalchemy import (
    select, insert, delete, text, asc, func
)


async def db_empty(app):
    """
    Check for db emptiness.
    Key arguments:
    app -- our application

    returns True/False depending on db emptiness
    """
    async with app['db'].acquire() as conn:
        query = text("SELECT True FROM tokens LIMIT(1)")
        return False if await conn.fetch(query) else True


async def on_start(app):
    """
    When the application starts it will configure the database with
    options from the 'database_config' which are places at config.yaml.

    Key arguments:
    app -- our application
    """
    config = app['config']
    app['db'] = await asyncpgsa.create_pool(**config['database_config'])


async def insert_token_into_db(app, token):
    async with app['db'].acquire() as conn:
        query = insert(tokens).values(
            token=token
        )
        await conn.fetchrow(query)


async def delete_token_from_db(app, token):
    """Delete a token from database.

    Keywords arguments:
    app -- the application
    token -- the deleting token

    There are several implementations of this function.
    For instance, we'd inquire only one but huge request.
    Like that:
    DO $$
    BEGIN
    IF (SELECT token FROM tokens ORDER BY id ASC LIMIT 1) = <required-token> THEN
        RETURN DELETE FROM tokens WHERE token = <required-token>  RETURNING 't'
    ELSE IF (SELECT True FROM tokens WHERE token = <required-token>) = True THEN
        RETURN "I don't know how to return (specifically in what format) but I believe you can come up with this:)"
    ELSE
        RETURN 'f'
    END IF;
    END $$;
    However I used another way. I don't want to use big query like that, therefore I decide to split these queries
    within python script. May be it makes some influence onto performance due to several queries but difference is few.

    Returns whether the token is available and the token-self

    """
    async with app['db'].acquire() as conn:

        # Checks for the table emptiness.
        query = text("SELECT True FROM tokens LIMIT(1)")
        if await conn.fetch(query):

            # If the table isn't empty then acquiring the token placed at the first position.
            token_at_first_pos = await conn.fetch(select([tokens.c.token]).order_by(asc(tokens.c.id)).limit(1))

            # If the first-pos token coincides with the token passed as the argument specifically the
            # token which was passed as the user-token by a client.
            if token_at_first_pos[0]['token'] == token:

                # If all is fine then remove it from the table.
                query = delete(tokens).where(tokens.c.token == token).returning(tokens.c.token)
                await conn.fetch(query)

                # Returns following: (Both are true)
                # 1) Is the token available?
                # 2) Does the token coincides with the first token?
                return True, True

            # If passed token isn't first then check for the token availability at whole.
            elif await conn.fetch(select([tokens]).where(tokens.c.token == token)):

                # Return that token is available, but it isn't first.
                return True, False

            # Otherwise returns that the token passed by user isn't available.
            # (According the task it means "cheating")
            else:
                return False, False

        # Table is already empty. User need to get a token.
        else:
            return False, 'Table is empty'


async def get_all_tokens(app):
    """
    This function created for a js displaying function

    Keywords arguments:
    app -- the application

    returns all tokens in database
    """
    async with app['db'].acquire() as conn:
        query = select([tokens.c.token])
        result = await conn.fetch(query)
        return result


async def get_num_of_tokens(app):
    """
    This function returns number of tokens in db
    It uses only once in the Token.get for a position
    retrieving.

    Keywords arguments:
    app -- the application

    returns number of tokens/position
    """
    async with app['db'].acquire() as conn:
        query = select([func.count(tokens.c.token)])
        result = await conn.fetch(query)
        return result


async def on_shutdown(app):
    """
    When the application ends its work it will close the connection with database

    Key arguments:
    app -- our application
    """
    async with app['db'].acquire() as conn:
        query = delete(tokens)
        await conn.fetchrow(query)
        await conn.execute("ALTER SEQUENCE tokens_id_seq RESTART ")
    await app['db'].close()


