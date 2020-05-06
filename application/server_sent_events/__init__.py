"""The init.py for 'websockets' which contains the only permit for function's sharing.
"""

from .events import ws_updates

# Admitting permit for usage in other files to the sse_updates only.
__all__ = ('ws_updates',)