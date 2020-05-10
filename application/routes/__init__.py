"""The init.py for 'routes' which contains the only permit for function's sharing.
"""

from .base import setup_routes


# Admitting permit for usage in other files to the setup_routes only.
__all__ = ('setup_routes',)