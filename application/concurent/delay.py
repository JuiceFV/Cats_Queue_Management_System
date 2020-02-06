"""

"""
import asyncio
import asyncpgsa
from application.database import db
from sqlalchemy import select, asc, delete, text


async def start_delete_delay(app, delay):
    async with app['db'].acquire() as conn:
        query = text("SELECT True FROM tokens LIMIT(1)")
        if await conn.fetch(query):
            query = select([db.tokens.c.id]).order_by(asc(db.tokens.c.id)).limit(1)
            id_before_sleep = await conn.fetchval(query, column=0)
            await asyncio.sleep(delay)
            id_after_sleep = await conn.fetchval(query, column=0)
            if id_before_sleep == id_after_sleep:
                query = delete(db.tokens).where(db.tokens.c.id == id_before_sleep)
                await conn.fetchrow(query)
                asyncio.gather(start_delete_delay(app, delay))
