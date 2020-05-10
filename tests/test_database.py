"""Tests placed here tests database' functionality.
"""
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
import __path_changing
from application.database import db_empty, insert_token_into_db, delete_token_from_db, get_all_tokens, get_num_of_tokens
from application.app import create_app
from application.settings import load_config
from sqlalchemy import text
from application.QMS.tokengenerator import TokenGenerator


class TestDataBase(AioHTTPTestCase):
    """The class which contains methods which tests database's functions.
    """

    async def get_application(self):
        """Creates a test application.
        """
        app = await create_app(config=load_config())
        return app

    @unittest_run_loop
    async def test_db_empty_false(self):
        """Test db_empty() in case if database is not empty.
        """
        query = text("INSERT INTO tokens VALUES (1, 'A00')")
        async with self.app['db'].acquire() as conn:
            await conn.fetch(query)
        res = await db_empty(self.app)
        self.assertFalse(res)

        # I do not aware why but it makes tests much faster.
        # If you do - let me know in issue
        await self.client.post('/post-token', data={'token-field': 'A00'})

    @unittest_run_loop
    async def test_db_empty_true(self):
        """Test db_empty() in case if database is empty.
        """
        res = await db_empty(self.app)
        self.assertTrue(res)

    @unittest_run_loop
    async def test_db_insertion(self):
        """Test the function which insert a token into database.
        """
        expected = [1, 'A00']
        await insert_token_into_db(self.app, 'A00')
        query = text("SELECT * FROM tokens")
        async with self.app['db'].acquire() as conn:
            result = await conn.fetch(query)
            self.assertListEqual([result[0]['id'], result[0]['token']], expected)

    @unittest_run_loop
    async def test_db_proper_deletion(self):
        """Test the function which delete a token from database.
        Considering that token is the first one in database.
        """
        expected = [True, True]
        query = text("INSERT INTO tokens VALUES (1, 'A00')")
        async with self.app['db'].acquire() as conn:
            await conn.fetch(query)
        token_presence, token_accuracy = await delete_token_from_db(self.app, 'A00')
        res = [token_presence, token_accuracy]
        self.assertListEqual(res, expected)

    @unittest_run_loop
    async def test_db_wrong_turn_deletion(self):
        """Test the function which delete a token from database.
        Considering that token is not the first one in database.
        """
        expected = [True, False]
        query1 = text("INSERT INTO tokens VALUES (1, 'A00')")
        query2 = text("INSERT INTO tokens VALUES (2, 'A01')")
        async with self.app['db'].acquire() as conn:
            await conn.fetch(query1)
            await conn.fetch(query2)
        token_presence, token_accuracy = await delete_token_from_db(self.app, 'A01')
        res = [token_presence, token_accuracy]
        self.assertListEqual(res, expected)

    @unittest_run_loop
    async def test_db_cheater_deletion(self):
        """Test the function which delete a token from database.
        Considering that token doesn't exist a.k.a. user is a cheater.
        """
        expected = [False, False]
        query = text("INSERT INTO tokens VALUES (1, 'A00')")
        async with self.app['db'].acquire() as conn:
            await conn.fetch(query)
        token_presence, token_accuracy = await delete_token_from_db(self.app, 'A01')
        res = [token_presence, token_accuracy]
        self.assertListEqual(res, expected)

    @unittest_run_loop
    async def test_db_empty_deletion(self):
        """Test the function which delete a token from database when it is empty.
        """
        expected = [False, 'Table is empty']
        token_presence, token_accuracy = await delete_token_from_db(self.app, 'A00')
        res = [token_presence, token_accuracy]
        self.assertListEqual(res, expected)

    @unittest_run_loop
    async def test_get_all_tokens(self):
        """The test which checks the function retrieving all tokens.
        """
        expected = ['A00', 'A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09']
        tg = TokenGenerator()
        async with self.app['db'].acquire() as conn:
            for i in range(10):
                query = text("INSERT INTO tokens (token) VALUES ('{}')".format(tg.generate_new_token()))
                await conn.fetch(query)
        fetched_res = await get_all_tokens(self.app)
        res = []
        for i in fetched_res:
            res.append(i['token'])
        self.assertListEqual(res, expected)

    @unittest_run_loop
    async def test_get_num_of_tokens(self):
        """The test which checks function which gives us amount of tokens.
        """
        expected = 10
        tg = TokenGenerator()
        async with self.app['db'].acquire() as conn:
            for i in range(10):
                query = text("INSERT INTO tokens (token) VALUES ('{}')".format(tg.generate_new_token()))
                await conn.fetch(query)
        res = (await get_num_of_tokens(self.app))[0]['count_1']
        self.assertEqual(res, expected)



