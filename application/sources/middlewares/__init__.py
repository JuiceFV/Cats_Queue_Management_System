"""The __init__.py for 'middlewares' which contains the only permit for functions' sharing.
"""

from .mw import setup_middlewares

# Admitting permit for usage in other modules to the setup_middlewares only.
__all__ = ('setup_middlewares', )