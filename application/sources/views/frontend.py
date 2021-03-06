"""This file responsible for basic server' responses.

It contains two different classes:
1) Index - class has the only 'get' method which handling the index-page. In the case where tokens are exists it returns
   them as a list in purpose to represent them using JS. Also it starts a delay if the web-page refreshed within
   image representation.
2) Token - the basic class which responsible for the gist logic of the application. Where 'get' - returns a new token
   and 'post' - returns either an image or an error. However both of them check for a cheater.

"""
from aiohttp_jinja2 import template
from aiohttp import web
from ..database import base
import asyncio
from ..image_processing.img_handler import get_image_url
from ..concurrency import make_task, start_delete_delay, get_previous_task


class Index(web.View):
    """Class which handles index.html
    The class has the only 'get' function which returns the rendered web-page.
    Basic page. Renders templates using aiohttp_jinja2.

    """
    @template('index.html')
    async def get(self):
        """This method renders the template and returns it as a response.

        returns rendered_template and token_list for representation.
        """

        # In the case if there are tokens in database able for representation it returns them.
        token_list = await base.get_all_tokens(self.app)

        # Also if there were more than 64 tokens before the page refresh - we sending a request to sse server
        # to update the 'redundant_tokens' on client-side.
        self.app['sse_requests']['redundant_tokens_vis'][0] = True

        # If the web page has been refreshed until '/start-delay' called by user on client-side, we have to continue
        # with it.
        await go_on_with_delay(self)

        return {'token_list': token_list}


async def go_on_with_delay(request):
    """Start delay for the first token in database.

    returns the '200'-status as response from server.
    """
    # Start the timer for the next token
    # If user used his/her/its token until the out of the time
    # I want to close the task of the time counting (closing directly in Token.post).
    # Therefore I am using the function of creating the task placed at
    # ../sources/concurrency/taskconfigurator.py
    task = make_task(start_delete_delay, request.app, 60)
    asyncio.gather(task)
    return web.Response(status=200)


class Token(web.View):
    """The class responsible for tokens handling.
    It contains 2 methods where the first one handling a token posted by an user and returns a status with
    image (if status isn't an error).
    And second one handling a request from a client side and returns status with token (if status isn't an error)
    """

    async def post(self):
        """Token processing
         Within this function we handle a token. We check a token for the accuracy.
         There are 4 options:
         1) Token is integrally proper and we return an image (image url)
         2) Such token exists but it's not at first position then we return error with appropriating status
         3) Such token doesn't exist hence return cheating-error
         4) Data base is empty. This status was created for my own purposes, it's 3d option indeed.
         5) Also there is a prominent options which returns an error if an user is already banned
        """
        # A response. It represents a dictionary because I'ill translate to its json-format in JS.
        response = {}

        # Checking if a cliet-peer in the ban-list.
        if not self.app['ban_list'][1].get(self.transport.get_extra_info('peername')[0]):

            # Receive the data from the request, I mean his token.
            post_data = await self.post()

            # delete_token_from_db() makes an effort to delete the token from db
            # It returns two values:
            # 1) token_availability -- Is the token in database? (True/False)
            # 2) token_accuracy -- Does the token coincide with the first token. It receives bool except the case
            #                      when the database empty, in this way it appears as the string ('Table is empty')
            token_availability, token_accuracy = await base.delete_token_from_db(self.app, post_data['token-field'])

            # Check for the database emptiness
            if token_accuracy != 'Table is empty':

                # First case, whether the needed token is the first one?
                if token_availability and token_accuracy:

                    # How do I close a task? Follow link below:
                    # https://stackoverflow.com/questions/56823893/how-to-get-task-out-of-asyncio-event-loop-in-a-view
                    if closing_task := get_previous_task():
                        closing_task.cancel()

                    # If the token is first then we shall to prepare it for the reuse.
                    # The prepare_used_token() placed at ../sources/QMS/tokengenerator.py
                    self.app['new_token'].prepare_used_token(post_data['token-field'])

                    # For the accurate representation on client-side after page-refresh we need to remove first token
                    # from the list of redundant tokens if it exists ofc.
                    # (Brief explanation: We do this because the first token in the list sets as the last token of the
                    # fourth column in the queue representation of the web page.)
                    if self.app['sse_requests']['redundant_tokens_vis'][1]:
                        self.app['sse_requests']['redundant_tokens_vis'][1].pop(0)

                    # Sending a request to the sse for removing one element from queue on web page.
                    self.app['sse_requests']['update_queue_vis_remove'] = True

                    # Generate an image url.
                    img_url = get_image_url()
                    response.update({'status': 'success'})
                    response.update({'image_url': img_url})

                # The option where token is not first.
                elif token_availability:
                    response.update({'status': 'wrong_turn'})

                # The option where token is not within the queue.
                else:

                    # According the task we have to do something indelible with this piece of shit.
                    # I decided to block him forever. (uah-ha-ha-ha (Villainy laugh))
                    # Therefore retrieving a peer-information
                    peer = self.transport.get_extra_info('peername')
                    with open(self.app['ban_list'][0].name, 'a') as banlist_file:

                        # Shove the peer' ip into the file (.ip_banlist)
                        banlist_file.write(peer[0] + '\n')

                    # And updating the ban-list of the current server-session
                    self.app['ban_list'][1].update({peer[0]: 'banned'})
                    response.update({'status': 'cheater'})

            # The option where no tokens in database
            else:
                response.update({'status': 'db_empty'})

        # When a user in ban-list
        else:
            response.update({'status': 'banned'})

        return web.json_response(response)

    async def get(self):
        """Generate token and represent it.

        returns a generated token and its position for the js function of representation or the message if user banned.
        """

        # First, check if the peer in ban-list
        if not self.app['ban_list'][1].get(self.transport.get_extra_info('peername')[0]):

            # We need this check to get a point regard # of calls.
            # If it's 1st call therefore we need start delay task.
            # If it's not then we skip the delay starting.
            db_emptiness = await base.db_empty(self.app)

            # Generating & Inserting into database a token
            token = self.app['new_token'].generate_new_token()
            await base.insert_token_into_db(self.app, token)

            # Creating the first task (delay-task) for the token' popping
            if db_emptiness:
                task = make_task(start_delete_delay, self.app, 60)
                asyncio.gather(task)

            # retrieving a token position for the js function (display_queue_add)
            token_position = (await base.get_num_of_tokens(self.app))[0]['count_1']

            # If the token_position is bigger than 64 then we propelling a token into redundant tokens' list
            # For the representation queue after web-page refresh.
            if token_position > 64:
                self.app['sse_requests']['redundant_tokens_vis'][1].append(token)

            # Send request to sse in purpose to append a token in representation queue.
            # Besides we throwing a token and its position.
            self.app['sse_requests']['update_queue_vis_append'] = [True, token, token_position]

            return web.json_response({'status': 'ok', 'token': token})
        return web.json_response({'status': 'banned'})
