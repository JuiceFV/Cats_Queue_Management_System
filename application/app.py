from aiohttp import web
import jinja2
import aiohttp_jinja2
from .routes.base import setup_routes
from cryptography import fernet
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import base64


async def create_app():
    """Creates an application with routes and returns it.

    At this function:
    1) Creates an application.
    2) Creates a key for the session and ties it with application.
    3) Sets up jinja2 for the templates rendering.
    4) Sets static_root_url for the static files up. In template it will looks like that:
       '<script src="{{ static('dist/main.js') }}"></script>'.
    5) Sets routes up. Routes are defines at base.py.
    6) Returns created application.

    """
    app = web.Application()

    fernet_key = fernet.Fernet.generate_key()
    secrete_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secrete_key))

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('application', 'templates')
    )
    app['static_root_url'] = '/static'
    setup_routes(app)
    return app
