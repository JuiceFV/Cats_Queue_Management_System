"""

"""
from aiohttp import web
from application.views import frontend
from application.server_sent_events import send_request_for_queue_update


def setup_routes(app):
    app.add_routes(
                    [
                        web.get('/', frontend.Index.get, name='index'),
                        web.get('/get-token', frontend.Token.get, name='token-getter'),
                        web.post('/post-token', frontend.Token.post, name='image-getter'),
                        web.get('/update', send_request_for_queue_update)
                    ]
                   )

    # In the configuration file we set the 'run_type' as weather test nor debug nor release
    # I did it because of tests destination
    if app['config']['run_type'] == 'test':
        app.router.add_static('/static', '../application/static', name='static', show_index=True)
    else:
        app.router.add_static('/static', 'application/static', name='static', show_index=True)
