
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
from application.views.frontend import Index
from application.app import create_app
from application.settings import load_config


class AppTestCases(AioHTTPTestCase):

    async def get_application(self):
        app = await create_app(config=load_config())
        app.router.add_static('/static', '../application/static', name='static', show_index=True)
        return app

    @unittest_run_loop
    async def test_index(self):
        resp = await self.client.request("GET", "/")
        assert resp.status == 200

