"""
This file contains the only function which starting a delay
for each token.
"""

import asyncio
from .taskconfig import make_task
from application.database import db
from sqlalchemy import select, asc, delete, text


async def start_delete_delay(app, delay):
    """
    The very function which thrust a delay for each front token.
    Key arguments:
    app -- our application.
    delay -- a delay in seconds
    """
    async with app['db'].acquire() as conn:

        # First of all we need to check for database emptiness
        query = text("SELECT True FROM tokens LIMIT(1)")
        if await conn.fetch(query):

            # If database is not empty then we are processing a waiting delay.
            # First, fetching an id & related token from the first position (due to it queue) from database.
            query = select([db.tokens.c.id, db.tokens.c.token]).order_by(asc(db.tokens.c.id)).limit(1)
            query_result = await conn.fetchrow(query)

            # Retrieving an id and token
            id_before_sleep, token = query_result['id'], query_result['token']

            # Setting a delay
            try:
                await asyncio.sleep(delay)

            # Some information related with cancellation error
            # https://docs.python.org/3/library/asyncio-task.html#asyncio.Task.cancel
            except asyncio.CancelledError:
                pass

            # Check whether a token at the first place as same as it was before
            finally:

                # If it possible but all of members picked their tokens over 60 seconds.
                if await conn.fetch(text("SELECT True FROM tokens LIMIT(1)")):
                    query_result = await conn.fetchrow(query)
                    id_after_sleep = query_result['id']

                    # If they are same then we delete that token and starting delay again.
                    if id_before_sleep == id_after_sleep:
                        query = delete(db.tokens).where(db.tokens.c.id == id_before_sleep)

                        # preparing a token for reuse.
                        app['new_token'].prepare_used_token(token)

                        # Deleting a token
                        await conn.fetchrow(query)

                        # Setting the flag to on, it means that we updating
                        # a queue. And SSE catching and handling it by checking this variable every second.
                        app['request_for_queue_update_vis'] = True

                        if app['redundant_tokens_vis'][1]:
                            app['redundant_tokens_vis'][1].pop(0)

                        # Starting a delay for adjacent token, over and over and over
                        task = make_task(start_delete_delay, app, delay)
                        asyncio.gather(task)