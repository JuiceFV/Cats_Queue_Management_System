"""Here we are setting up the routes .
"""
from aiohttp import web
from pathlib import Path
from ..views import frontend, go_on_with_delay
from ..server_sent_events import sse_updates


def setup_routes(app):
    """ The only function which sets application's routes up.
    """
    path_to_static = Path(__file__).parent.parent / "static"
    app.add_routes(
                    [
                        web.get('/', frontend.Index.get, name='index'),
                        web.get('/get-token', frontend.Token.get, name='token-getter'),
                        web.post('/post-token', frontend.Token.post, name='image-getter'),
                        web.get('/update', sse_updates, name='sse'),
                        web.get('/start-delay', go_on_with_delay, name="continue_delay"),
                        web.static('/static', path_to_static, name='static', show_index=True)
                    ]
                   )
