"""The init.py for 'database' which contains the only permit for function's sharing.
"""

from .base import on_start, insert_token_into_db, on_shutdown, db_empty, get_all_tokens, get_num_of_tokens

# Admitting permit for usage in other files to the the following functions.
__all__ = ('on_start', 'insert_token_into_db', 'on_shutdown', 'db_empty', 'get_all_tokens', 'get_num_of_tokens')
