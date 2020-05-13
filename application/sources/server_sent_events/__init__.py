"""The __init__.py for 'server_sent_events' which contains the only permit for functions' sharing.
"""

from .events import sse_updates

# Admitting permit for usage in other modules to the sse_updates only.
__all__ = ('sse_updates',)