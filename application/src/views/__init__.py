"""The init.py for 'views' which contains the only permit for function's sharing.
"""
from .frontend import Index, Token, go_on_with_delay

# Giving permit for these functions/classes
__all__ = ('Index', 'Token', 'go_on_with_delay')