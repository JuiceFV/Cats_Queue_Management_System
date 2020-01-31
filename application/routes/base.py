from aiohttp import web
from application.views import frontend


def setup_routes(app):
    app.add_routes(
                    [
                        web.get('/', frontend.Index.get),
                        web.static('/static', 'application/static', name='static', show_index=True),
                        web.get('/get-token', frontend.Token.get)
                    ]
                   )
