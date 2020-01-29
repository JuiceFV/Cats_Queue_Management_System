from aiohttp_jinja2 import template
from aiohttp import web
from aiohttp_session import get_session
from datetime import datetime


class Index(web.View):

    @template('index.html')
    async def get(self):
        return {}


# class Kitty(web.View):
#
#     async def post(self):
#         token = await self.post()
#         print(token['token'])
#         return web.HTTPFound('/')