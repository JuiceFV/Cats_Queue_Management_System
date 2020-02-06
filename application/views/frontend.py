"""

"""
from aiohttp_jinja2 import template
from aiohttp import web
from ..database import base
from application.concurent.delay import start_delete_delay
import asyncio


class Index(web.View):
    """Class which handles index.html

    Basic page. Renders templates using aiohttp_jinja2.

    """
    @template('index.html')
    async def get(self):
        return {}


class Token(web.View):

    # TODO think how to optimize

    async def post(self):
        """Token processing

        """
        post_data = await self.post()
        if len(post_data['token-field']) == 0:
            # delete_token_from_db() makes an effort to delete the token from db
            # It returns two values:
            # 1) token_accurate -- Does the token coincide with the first token from db. (Possible values: True/False)
            # 2) token -- the value of the token or (if token_accurate == False) it returns True/False
            #             depends on token availability.
            token_accurate, token = await base.delete_token_from_db(self.app, post_data['token-field'])

            if token_accurate:
                self.app['new_token'].prepare_used_token(token)
                asyncio.gather(start_delete_delay(self.app, 30))
                """
                Some code ...
                """
                return web.json_response({'status': 'success'})
            elif token:
                """
                Some code ...
                """
                return web.json_response({'status': 'Not your turn.'})
            else:
                """
                Some code ...
                """
                return web.json_response({'status': 'Cheater'})
        else:
            return web.json_response({'status': 'Empty field'})

    async def get(self):
        """Generate token and represent it.

        """
        token = self.app['new_token'].generate_new_token()
        # TODO Fix token == 'A00' due to 'A00' uses many times.
        if token == 'A00':
            asyncio.gather(start_delete_delay(self.app, 30))
        await base.insert_token_into_db(self.app, token)
        return web.json_response({'token': token})
