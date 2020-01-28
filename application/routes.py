from aiohttp import web
from .views import frontend


def setup_rotes(app):
    app.add_routes(
                    [
                        web.get('/', frontend.index),
                        web.static('/static', 'application/static', name='static', show_index=True)
                    ]
                   )
