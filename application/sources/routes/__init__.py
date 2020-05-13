"""The __init__.py for 'routes' which contains the only permit for functions' sharing.
"""

from .base import setup_routes


# Admitting permit for usage in other modules to the setup_routes only.
__all__ = ('setup_routes',)