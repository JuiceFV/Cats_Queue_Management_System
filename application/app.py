from aiohttp import web
import logging
import jinja2
import aiohttp_jinja2
from .routes.base import setup_routes
from cryptography import fernet
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from .database.base import on_start, on_shutdown
import base64
from .QMS.tokengenerator import TokenGenerator


async def create_app(config: dict):
    """Creates an application with routes and returns it.

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

    app.on_startup.append(on_start)
    app.on_cleanup.append(on_shutdown)

    return app

