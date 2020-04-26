"""

"""
from aiohttp import web
from application.views import frontend, go_on_with_delay
from application.server_sent_events import sse_updates


def setup_routes(app):
    app.add_routes(
                    [
                        web.get('/', frontend.Index.get, name='index'),
                        web.get('/get-token', frontend.Token.get, name='token-getter'),
                        web.post('/post-token', frontend.Token.post, name='image-getter'),
                        web.get('/update', sse_updates, name='sse'),
                        web.get('/start-delay', go_on_with_delay)
                    ]
                   )

    # In the configuration file we set the 'run_type' as weather test nor debug nor release
    # I did it because of tests destination
    if app['config']['run_type'] == 'test':
        app.router.add_static('/static', '../application/static', name='static', show_index=True)
    else:
        app.router.add_static('/static', 'application/static', name='static', show_index=True)
