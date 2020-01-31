from aiohttp_jinja2 import template
from aiohttp import web
from ..database import base


class Index(web.View):
    """Class which handles index.html


    """
    @template('index.html')
    async def get(self):
        return {}


class Token(web.View):

    async def post(self):
        pass

    async def get(self):
        data = {'token': self.app['new_token'].generate_new_token()}
        """ Add token into database
        
        ...
        
        """
        return web.json_response(data)
