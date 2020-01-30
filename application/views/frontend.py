from aiohttp_jinja2 import template
from aiohttp import web
from ..QMS.tokenqueue import Token
from ..database import base


class Index(web.View):
    """Class which handles index.html


    """
    @template('index.html')
    async def get(self):
        return {}


class TokenHandler(web.View):

    async def get(self):
        pass
