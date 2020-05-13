"""The file contains tests which checks for proper middleware handling.
"""
import __path_changing
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from sources.app import create_app
from sources.settings import load_config
from aiohttp import web


class TestMiddlewares(AioHTTPTestCase):
    """The class which tests the middlewares response.
    """

    async def get_application(self):
        """Creates an application.
        """
        async def req_404(request):
            """Returns 404 HTTP Exception.
            """
            return web.HTTPNotFound()

        async def req_500(request):
            """Returns 500 HTTP Exception.
            """
            return web.HTTPInternalServerError()

        async def req_400(request):
            """Returns 400 HTTP Exception.
            """
            return web.HTTPBadRequest()

        app = await create_app(config=load_config())
        app.add_routes([web.get('/400-error', req_400)])
        app.add_routes([web.get('/500-error', req_500)])
        app.add_routes([web.get('/404-error', req_404)])
        return app

    @unittest_run_loop
    async def test_400_error(self):
        """Test for proper HTTP:400 return.
        """
        resp = await self.client.request('GET', '/400-error')
        assert resp.status == 200
        resp = await resp.text()
        assert 'src="/static/images/400.jpg"' in resp

    @unittest_run_loop
    async def test_404_error(self):
        """Test for proper HTTP:404 return.
        """
        resp = await self.client.request('GET', '/404-error')
        assert resp.status == 200
        resp = await resp.text()
        assert 'src="/static/images/404.jpg"' in resp

    @unittest_run_loop
    async def test_500_error(self):
        """Test for proper HTTP:500 return.
        """
        resp = await self.client.request('GET', '/500-error')
        assert resp.status == 200
        resp = await resp.text()
        assert 'src="/static/images/500.jpg"' in resp
