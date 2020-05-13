"""This module/file whatever you want aims to help us to structure asyncio tasks.
"""

import asyncio

# The list of asyncio tasks which needed to be canceled or modified or something else.
_tasks = []


def make_task(coroutine_function, *coroutine_args):
    """This function creates and appends a task into the tasks-list.

    Key Arguments:
    coroutine_function -- an async-function which needed to be under surveillance.
    *coroutine_args -- arguments for the function above.

    Returns created task.
    """
    async def wrapped_coroutine():
        """This function launches a coroutine and when it's over we removing a task from the list.
        """
        try:
            return await coroutine_function(*coroutine_args)
        finally:
            if len(_tasks) != 0:
                del _tasks[0]
    task = asyncio.create_task(wrapped_coroutine())
    _tasks.append(task)
    return task


def get_previous_task():
    """This function returns first task in the queue.
    """
    return _tasks[0] if len(_tasks) != 0 else None

