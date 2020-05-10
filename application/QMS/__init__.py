"""The init.py for 'QMS' which contains the only permit for function's sharing.
"""

from .tokengenerator import TokenGenerator

# Admitting permit for usage in other files to the TokenGenerator only.
__all__ = ('TokenGenerator',)