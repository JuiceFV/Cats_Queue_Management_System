"""This module contains merely the only function responsible for sse interaction.
"""

import asyncio
from aiohttp_sse import sse_response


async def sse_updates(request):
    """Exactly this function which responsible for sse requests.
    """
    loop = request.app.loop
    async with sse_response(request) as resp:

        # Listen for events each 10 ms.
        while True:

            # Sending request for queue' token remove when it's been removed on server.
            if request.app['sse_requests']['update_queue_vis_remove']:
                await resp.send("update-remove")
                request.app['sse_requests']['update_queue_vis_remove'] = False

            # Sending request for queue' token adding up when it's been added on server.
            if request.app['sse_requests']['update_queue_vis_append'][0]:
                await resp.send(f"update-append {request.app['sse_requests']['update_queue_vis_append'][1]} {request.app['sse_requests']['update_queue_vis_append'][2]}")
                request.app['sse_requests']['update_queue_vis_append'][0] = False

            # Sending request for redundant token's list rewrite (on client side ofc)
            if request.app['sse_requests']['redundant_tokens_vis'][0]:
                await resp.send('update-redtokens ' + ''.join(token + ' ' for token in request.app['sse_requests']['redundant_tokens_vis'][1]))
                request.app['sse_requests']['redundant_tokens_vis'][0] = False

            await asyncio.sleep(0.1, loop=loop)
    return resp

