"""Tests placed here checks functions responsible for delay removing token that out of waiting time, and
responsible for task's making and related functions
"""
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
import __path_changing
from src.concurrency import start_delete_delay
from src.concurrency.taskconfig import _tasks, make_task, get_previous_task
from src.app import create_app
from src.settings import load_config
from sqlalchemy import text
import asyncio


class TestDelayAndMakeTask(AioHTTPTestCase):
    """The class which tests the function related with delete tokens after a delay.
    """

    async def get_application(self):
        """Creates a test application.
        """
        app = await create_app(config=load_config())
        return app

    @unittest_run_loop
    async def test_users_doesnt_use_token(self):
        """Test delete's delay onto 2 users which didn't use their tokens.
        """
        expected = []

        # Inserting two tokens into database.
        query1 = text("INSERT INTO tokens (token) VALUES ('A00')")
        query2 = text("INSERT INTO tokens (token) VALUES ('A01')")
        async with self.app['db'].acquire() as conn:
            await conn.fetch(query1)
            await conn.fetch(query2)

            # Starting the delay equals 1 second for each task
            # The whole time of waiting is ~2 (a little bit more than 2) seconds
            asyncio.gather(start_delete_delay(self.app, 1))

            # Emulating users's delay for 3 seconds
            await asyncio.sleep(3)
            query = text("SELECT * FROM tokens")
            res = await conn.fetch(query)
            self.assertListEqual(expected, res)

    @unittest_run_loop
    async def test_users_use_token(self):
        """Test delete's delay onto 2 users where one of them used his/her/its token.
        """
        expected = 'A01'
        expected_prepared_token = 'A00'

        # Inserting two tokens into database.
        query1 = text("INSERT INTO tokens (token) VALUES ('A00')")
        query2 = text("INSERT INTO tokens (token) VALUES ('A01')")
        async with self.app['db'].acquire() as conn:
            await conn.fetch(query1)
            await conn.fetch(query2)

            # Starting the delay equals 2 second for each task
            # The whole time of waiting is ~4 (a little bit more than 4) seconds
            asyncio.gather(start_delete_delay(self.app, 2))

            # Emulating users's delay for 3 seconds
            await asyncio.sleep(3)
            query = text("SELECT * FROM tokens")
            res = (await conn.fetch(query))[0]['token']
            self.assertEqual(expected, res)

            # A popped token, specifically 'A00' should become as ready for reuse.
            self.assertEqual(expected_prepared_token, ''.join(self.app['new_token'].tokens_ready_to_present[0]))

    @unittest_run_loop
    async def test_make_task(self):
        """The test which checks the function created for proper task cancellation.
        """
        query1 = text("INSERT INTO tokens (token) VALUES ('A00')")
        async with self.app['db'].acquire() as conn:
            await conn.fetch(query1)

            # Creates a task and push it into the task-list ('_tasks')
            # in purpose to close it after 'start_delete_delay' is over.
            task = make_task(start_delete_delay, self.app, 1)
            asyncio.gather(task)
            self.assertEqual(1, len(_tasks))
            await asyncio.sleep(2)

            # When a task is over it should be removed from task-list ('_tasks')
            self.assertEqual(0, len(_tasks))

    @unittest_run_loop
    async def test_get_previous_task(self):
        """It seems hilarious but I also check the function which returns first task from task-list.
        """
        query1 = text("INSERT INTO tokens (token) VALUES ('A00')")
        query2 = text("INSERT INTO tokens (token) VALUES ('A01')")
        async with self.app['db'].acquire() as conn:
            await conn.fetch(query1)
            await conn.fetch(query2)
            task = make_task(start_delete_delay, self.app, 1)
            asyncio.gather(task)
            # Letting the second task be launched and pushed into the task-list.
            await asyncio.sleep(2)
            self.assertEqual(get_previous_task(), _tasks[0])
