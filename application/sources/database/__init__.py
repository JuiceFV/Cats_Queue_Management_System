"""The __init__.py for 'database' which contains the only permit for functions' sharing.
"""

from .base import on_start, insert_token_into_db, on_shutdown, db_empty, get_all_tokens, get_num_of_tokens,\
    delete_token_from_db

# Admitting permit for usage in other modules to the the following functions.
__all__ = ('on_start', 'insert_token_into_db', 'on_shutdown', 'db_empty', 'get_all_tokens', 'get_num_of_tokens',
           'delete_token_from_db',)
