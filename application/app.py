from aiohttp import web
import jinja2
import aiohttp_jinja2
from .routes import setup_rotes


async def create_app():
    """Creates an application with routes and returns it.

    At this function:
    1) Creates an application.
    2) Sets up jinja2 for the templates rendering.
    3) Sets static_root_url for the static files up. In template it will looks like that:
       '<script src="{{ static('dist/main.js') }}"></script>'.
    4) Sets routes up. Routes are defines at routes.py.
    5) Returns created application.

    """
    app = web.Application()
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('application', 'templates')
    )
    app['static_root_url'] = '/static'
    setup_rotes(app)
    return app
