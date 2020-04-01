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
        query = text("SELECT True FROM tokens LIMIT(1)")
        if await conn.fetch(query):
            query = select([db.tokens.c.id]).order_by(asc(db.tokens.c.id)).limit(1)
            id_before_sleep = await conn.fetchval(query, column=0)
            try:
                await asyncio.sleep(delay)

            # Some information related with cancellation error
            # https://docs.python.org/3/library/asyncio-task.html#asyncio.Task.cancel
            except asyncio.CancelledError:
                pass
            finally:
                id_after_sleep = await conn.fetchval(query, column=0)
                if id_before_sleep == id_after_sleep:
                    query = delete(db.tokens).where(db.tokens.c.id == id_before_sleep)
                    if await conn.fetch(text("SELECT True FROM tokens LIMIT(1)")):
                        await conn.fetchrow(query)
                        task = make_task(start_delete_delay, app, delay)
                        asyncio.gather(task)