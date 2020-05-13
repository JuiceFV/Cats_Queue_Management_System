"""The __init__.py for 'concurrency' which contains the only permit for functions' sharing.
"""

from .taskconfig import make_task, get_previous_task
from .timer import start_delete_delay

# Admitting permit for usage in other modules to the the following functions.
__all__ = ('make_task', 'start_delete_delay', 'get_previous_task',)