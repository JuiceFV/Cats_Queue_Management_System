"""Here is placed the function which configures an application.

Import packages:
jinja2 --
bas64 --
logging --
aiohttp_jinja2 --
aiohttp.web --
cryptography.fernet --
aiohttp_session.setup --
.routes.base.setup_routes --
.QMS.tokengenerator.TokenGenerator --
.database.base.on_start/on_shutdown --
aiohttp_session.cookie_storage.EncryptedCookieStorage --

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
    app['config'] = config
    app['update_queue_vis'] = False
    app['ban_list'] = {}
    app['new_token'] = TokenGenerator()

    # Adding logging
    # The only option where logs are invisible is 'release'
    if app['config']['run_type'] != 'release':
        logging.basicConfig(level=logging.DEBUG)

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
