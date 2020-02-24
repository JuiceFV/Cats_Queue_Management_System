"""

"""
from aiohttp_jinja2 import template
from aiohttp import web
from ..database import base
import asyncio
from ..image_processing.img_handler import get_image_url


class Index(web.View):
    """Class which handles index.html

    Basic page. Renders templates using aiohttp_jinja2.

    """
    @template('index.html')
    async def get(self):
        return {}


class Token(web.View):

    async def post(self):
        """Token processing

        """
        # Receive the data from the request
        post_data = await self.post()

        # The response depended on post_data accuracy.
        response = {}

        # delete_token_from_db() makes an effort to delete the token from db
        # It returns two values:
        # 1) token_availability -- Is the token in the database? (True/False)
        # 2) token_accuracy -- Does the token coincides with the first token. It receives (True/False) except the case
        #                      when the data base empty in this way it appears as the string ('Table is empty')
        token_availability, token_accuracy = await base.delete_token_from_db(self.app, post_data['token-field'])

        # Check for the database emptiness
        if token_accuracy != 'Table is empty':

            # First case, whether the needed toke is first one?
            if token_availability and token_accuracy:

                # TODO Close tasks
                # https://stackoverflow.com/questions/56823893/how-to-get-task-out-of-asyncio-event-loop-in-a-view
                # if closing_task := get_task():
                #     closing_task.cancel()

                # If the token is first then we shall to prepare it for the reuse.
                # The prepare_used_token() is placed at ../application/QMS/tokengenerator.py
                self.app['new_token'].prepare_used_token(post_data['token-field'])

                # Start the timer for the next token
                # If user used his/her/its token until the out of the time I want to close the task of the time counting
                # Therefore I using the function of creating the task placed at
                # ../application/concurent/taskconfigurator.py
                # TODO cancel error w/ many tokens
                if not await base.db_empty(self.app):
                    print("""
                                The timer for the non-first token begins\n
                                task = make_task(start_delete_delay, self.app, 35)\n
                                asyncio.gather(task)
                                """)

                """
                Some code ...
                """
                img_url = get_image_url()
                response.update({'status': 'success'})
                response.update({'image_url': img_url})
            elif token_availability:
                """
                Some code ...
                """
                response.update({'status': 'wrong_turn'})
            else:
                """
                Some code ...
                """
                response.update({'status': 'cheater'})
        else:
            response.update({'status': 'db_empty'})

        return web.json_response(response)

    async def get(self):
        """Generate token and represent it.

        """
        db_emptiness = await base.db_empty(self.app)
        token = self.app['new_token'].generate_new_token()
        await base.insert_token_into_db(self.app, token)
        # Check is there the tokens needed to be popped.
        if db_emptiness:
            print("""
            The timer for the first token begins\n
            task = make_task(start_delete_delay, self.app, 35)\n
            asyncio.gather(task)
            """)
        return web.json_response({'token': token})
