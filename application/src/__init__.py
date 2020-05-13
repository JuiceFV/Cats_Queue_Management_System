"""The init.py for 'application' which contains the only permit for function's sharing.
"""

from .app import create_app

# Admitting permit for usage in other files to the create_app only.
__all__ = ('create_app',)