"""The __init__.py for 'QMS' which contains the only permit for functions' sharing.
"""

from .tokengenerator import TokenGenerator

# Admitting permit for usage in other modules to the TokenGenerator only.
__all__ = ('TokenGenerator',)