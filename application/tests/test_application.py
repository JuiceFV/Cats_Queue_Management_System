"""The file contains tests related with application's basic methods and accurate variable's set.
Do not change 3 very last tests' position. (It checks for a correct behavior with cheater and banned
users therefore the behavior of other tests may fickle if you change their the placement.)
"""
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
import sys
import os

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from sources.app import create_app
from sources.settings import load_config
from sources.QMS.tokengenerator import TokenGenerator


class TestApplication(AioHTTPTestCase):
    """Test application, especially its basic functions and methods.
    """

    async def get_application(self):
        """Creates a test application.
        """
        app = await create_app(config=load_config())
        return app

    @unittest_run_loop
    async def test_created_app(self):
        """Sends the basic request to the index-page.
        """
        resp = await self.client.get('/')
        assert resp.status == 200

    def test_run_type(self):
        """Testing for the correct run-type.
        """
        self.assertEqual('test', self.app['config']['run_type'])

    def test_set_variables(self):
        """Test for application' global variables.
        """
        expected_session_list = []
        expected_sse_requests = {
            'update_queue_vis_append': [False, None, None],
            'update_queue_vis_remove': False,
            'redundant_tokens_vis': [False, []]
        }
        expected_new_token = TokenGenerator()
        expected_config = \
            {
                'database_config':
                    {
                        'host': 'localhost',
                        'user': 'postgres',
                        'password': '12345qwerty',
                        'port': 5432,
                        'database': 'CatsQMS'
                    },
                'run_type': 'test'
            }
        self.assertEqual(expected_session_list, self.app['sessions_list'])
        self.assertEqual(expected_sse_requests, self.app['sse_requests'])
        self.assertEqual(type(expected_new_token), type(self.app['new_token']))
        self.assertEqual(expected_config, self.app['config'])

    @unittest_run_loop
    async def test_get_index(self):
        """Test for the correct either very first nor refresh page.
        """
        resp = await self.client.get('/')
        assert resp.status == 200
        result = await resp.text()
        assert '<title>Kitty Getter</title>' in result

    @unittest_run_loop
    async def test_get_token_ordinary_behavior(self):
        """Tests which checks for token's obtaining.
        """
        resp = await self.client.get("/get-token")
        assert resp.status == 200
        resp = await resp.json()
        self.assertEqual('A00', resp['token'])

        # I do not aware why but it makes tests much faster.
        # If you do - let me know in issue
        await self.client.post('/post-token', data={'token-field': 'A00'})

    @unittest_run_loop
    async def test_get_multiple_tokens_ordinary_behavior(self):
        """Tests which checks for multiple tokens requested one by one.
        """
        expected = ['A00', 'A01', 'A02', 'A03', 'A04', 'A05']
        res = []
        for i in range(0, 6):
            resp = await self.client.get("/get-token")
            if resp.status == 200:
                resp = await resp.json()
                res.append(resp['token'])
        self.assertListEqual(expected, res)

        # I do not aware why but it makes tests much faster.
        # If you do - let me know in issue
        await self.client.post('/post-token', data={'token-field': 'A00'})

    @unittest_run_loop
    async def test_get_unordered_multiple_tokens_ordinary_behavior(self):
        """Tests which checks for multiple tokens requested not one by one
        """
        expected = ['A01', 'A02', 'A03', 'A04', 'A05', 'A00', 'A06']
        res = []

        # First of all, 6 users take their tokens and turns into a queue.
        for i in range(0, 6):
            resp = await self.client.get("/get-token")
            if resp.status == 200:
                resp = await resp.json()
                res.append(resp['token'])

        # Then the first user uses his/her/its token, therefore he outs from a queue.
        resp = await self.client.post("/post-token", data={'token-field': 'A00'})
        if resp.status == 200:
            res.remove('A00')

        # And, finally, the lat user (7th user) takes his/her/its token and turns into a queue.
        resp = await self.client.get("/get-token")
        if resp.status == 200:
            resp = await resp.json()
            res.append(resp['token'])

        # I decided to take another one in purpose to prove it remains from the place where it's been finished.
        resp = await self.client.get("/get-token")
        if resp.status == 200:
            resp = await resp.json()
            res.append(resp['token'])

        self.assertListEqual(expected, res)

    @unittest_run_loop
    async def test_post_token_ordinary_behavior(self):
        """This test checks for post proper (it means when an user passed the precise token) behavior.
        """

        # Just sending a request for the first token and using it for getting an image.
        resp = await self.client.get("/get-token")
        if resp.status == 200:
            resp = await self.client.post("/post-token", data={'token-field': 'A00'})
            result = await resp.json()
            self.assertEqual('success', result['status'])

        # Just sending two requests (one by one) for the tokens and using them for getting images (one by on ofc).
        resp = await self.client.get("/get-token")
        if resp.status == 200:

            resp = await self.client.get("/get-token")
            if resp.status == 200:

                resp = await self.client.post("/post-token", data={'token-field': 'A00'})
                result = await resp.json()
                self.assertEqual('success', result['status'])

                resp = await self.client.post("/post-token", data={'token-field': 'A01'})
                result = await resp.json()
                self.assertEqual('success', result['status'])

    @unittest_run_loop
    async def test_post_token_db_empty(self):
        """The test in case when no one got their token.
        """
        resp = await self.client.post("/post-token", data={'token-field': 'A01'})
        resp = await resp.json()
        self.assertEqual('db_empty', resp['status'])

    @unittest_run_loop
    async def test_post_token_wrong_turn(self):
        """The test-case when an user makes an effort to get an image at not its turn.
        """
        await self.client.get('/get-token')
        await self.client.get('/get-token')
        resp = await self.client.post("/post-token", data={'token-field': 'A01'})
        resp = await resp.json()
        self.assertEqual('wrong_turn', resp['status'])

        # I do not aware why but it makes tests much faster.
        # If you do - let me know in issue
        await self.client.post('/post-token', data={'token-field': 'A00'})

    @unittest_run_loop
    async def test_banned_get_token(self):
        """This test the response if an user banned.
        """

        # Emulating an user's ban
        self.app['ban_list'][1].update({'127.0.0.1': 'banned'})
        resp = await self.client.get('/get-token')
        if resp.status == 200:
            resp = await resp.json()
            self.assertEqual('banned', resp['status'])

    @unittest_run_loop
    async def test_post_token_user_get_banned(self):
        """The test in case when an user tries to get image whilst being banned.
        """
        # Emulating an user's ban
        self.app['ban_list'][1].update({'127.0.0.1': 'banned'})
        resp = await self.client.post("/post-token", data={'token-field': 'A01'})
        resp = await resp.json()
        self.assertEqual('banned', resp['status'])

    @unittest_run_loop
    async def test_post_token_cheater(self):
        """The test in case when an user is cheater and he/she/it is not banned, yet.
        Note: After this test-case remove your ip from '.ip-banlist'
        """
        await self.client.get('/get-token')
        resp = await self.client.post("/post-token", data={'token-field': 'A01'})
        resp = await resp.json()
        self.assertEqual('cheater', resp['status'])
