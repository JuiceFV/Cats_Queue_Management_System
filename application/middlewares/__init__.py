"""The init.py for 'middlewares' which contains the only permit for function's sharing.
"""

from .mw import setup_middlewares

# Admitting permit for usage in other files to the setup_middlewares only.
__all__ = ('setup_middlewares', )