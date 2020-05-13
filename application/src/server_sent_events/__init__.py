"""The init.py for 'server_sent_events' which contains the only permit for function's sharing.
"""

from .events import sse_updates

# Admitting permit for usage in other files to the sse_updates only.
__all__ = ('sse_updates',)