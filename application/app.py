"""Here is placed the function which configures an application.



Functions:
create_app(config: dict) --

"""


import jinja2
import base64
import logging
import aiohttp_jinja2
from aiohttp import web
from cryptography import fernet
from .QMS import TokenGenerator
from .routes import setup_routes
from aiohttp_session import setup
from .middlewares import setup_middlewares
from .database import on_start, on_shutdown
from aiohttp_session.cookie_storage import EncryptedCookieStorage


def detecting_runtype(app):
    """This function checks for the correct run-type.
    There are 3 possible run-types: debug/release/test

    Keywords arguments:
    app -- the application
    """

    # If a run-type doesn't coincide with 3 following run-types then we're raising custom exception.
    if app['config']['run_type'] != 'release' and \
       app['config']['run_type'] != 'debug' and \
       app['config']['run_type'] != 'test':
        try:
            raise Exception('Wrong run-type', app['config']['run_type'])
        except Exception as inst:
            error, user_input = inst.args
            print(f'{error}: You passed {user_input} as run-type.')
            raise

    # If the we deploy the application then we turn off logging
    if app['config']['run_type'] != 'release':
        logging.basicConfig(level=logging.DEBUG)


def setup_application_variables(app, config):
    """This function sets up global variables (global for the app)

    Keywords arguments:
    app -- the application
    config -- a configuration extracted form config-file
    """

    # Setting configuration
    app['config'] = config

    # Here we'ill contain the ban-list
    # index==0 - the file where ip' are placed constantly
    # index==1 - the dictionary where ip' are placed temporary (Because, Dict-Find complexity is O(1))
    app['ban_list'] = [open(".ip_banlist", 'r')]
    app['ban_list'].append({ip.strip(): 'banned' for ip in app['ban_list'][0]})

    # A token, specifically novel generated
    app['new_token'] = TokenGenerator()

    app['sse_requests'] = {
        'update_queue_vis_append': [False, None, None],
        'update_queue_vis_remove': False,
        'redundant_tokens_vis': [False, []]
    }


async def create_app(config: dict):
    """Creates an application with routes and returns it.

    Keywords arguments:
    config:dict -- the configuration passed as argument or default configuration at "application" - directory.

    returns created application
    """

    # Creating an application
    app = web.Application()

    # Importing a config into the application
    # Then creating the global variable responsible for queue representation, specifically auto-removing
    # Also creating the global variable responsible for a token
    setup_application_variables(app, config)

    # It's checking for a run-type. There are ONLY 3 options debug/release/test
    detecting_runtype(app)

    # Adding key specifying an each session
    fernet_key = fernet.Fernet.generate_key()
    secrete_key = base64.urlsafe_b64decode(fernet_key)

    # Setting up this key for the application
    setup(app, EncryptedCookieStorage(secrete_key))

    # Setting template loader
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('application', 'templates')
    )

    # Setting up the route for the static files.
    app['static_root_url'] = '/static'

    # Setting up the routes specified at ./routes/base.py
    setup_routes(app)

    # Setting up the routes specified at ./middlewares/mw.py
    setup_middlewares(app)

    # Uploading and starting a database on application starts
    app.on_startup.append(on_start)

    # TODO ADD close remains tasks on_cleanup

    # Cleaning up a database on application shutdown.
    app.on_cleanup.append(on_shutdown)

    return app
