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

    At this function:
    1) Creates an application.
    2) Creates a key for the session and ties it with application.
    3) Sets up jinja2 for the templates rendering.
    4) Sets static_root_url for the static files up. In template it will looks like that:
       '<script src="{{ static('dist/main.js') }}"></script>'.
    5) Sets routes up. Routes are defines at base.py.
    6) Configures database
    7) Closes all connections with database
    8) Returns created application.

    """
    app = web.Application()

    app['config'] = config
    app['new_token'] = TokenGenerator()
    # Adding logging
    logging.basicConfig(level=logging.DEBUG)

    fernet_key = fernet.Fernet.generate_key()
    secrete_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secrete_key))

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('application', 'templates')
    )

    app['static_root_url'] = '/static'

    setup_routes(app)

    setup_middlewares(app)

    app.on_startup.append(on_start)
    # ADD close remains tasks on_cleanup
    app.on_cleanup.append(on_shutdown)

    return app
