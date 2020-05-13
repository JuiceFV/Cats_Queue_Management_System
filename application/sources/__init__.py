"""The __init__.py for 'application' which contains the only permit for functions' sharing.
"""

from .app import create_app

# Admitting permit for usage in other modules to the create_app only.
__all__ = ('create_app',)