"""

"""
from aiohttp import web
from application.views import frontend


def setup_routes(app):
    app.add_routes(
                    [
                        web.get('/', frontend.Index.get),
                        web.get('/get-token', frontend.Token.get),
                        web.post('/post-token', frontend.Token.post),
                    ]
                   )

    # In the configuration file we set the 'run_type' as weather test nor debug nor release
    # I did it because of tests destination
    if app['config']['run_type'] == 'test':
        app.router.add_static('/static', '../application/static', name='static', show_index=True)
    else:
        app.router.add_static('/static', 'application/static', name='static', show_index=True)
