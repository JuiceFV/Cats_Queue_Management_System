"""This file contains merely the only function responsible for sse interaction.
"""

import asyncio
from aiohttp import web
#from aiohttp_session import get_session
#from aiohttp_sse import sse_response


async def ws_updates(request):
    """Exactly this function which responsible for sse requests.
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    request.app['ws_list'].append(ws)

    loop = request.app.loop
    while True:
        # Sending request for queue' token remove when it's been removed on server.
        if request.app['ws_requests']['update_queue_vis_remove']:
            for _ws in request.app['ws_list']:
                await _ws.send_str("update-remove")
            request.app['ws_requests']['update_queue_vis_remove'] = False

        # Sending request for queue' token adding up when it's been added on server.
        if request.app['ws_requests']['update_queue_vis_append'][0]:
            for _ws in request.app['ws_list']:
                await _ws.send_str(f"update-append {request.app['ws_requests']['update_queue_vis_append'][1]} {request.app['ws_requests']['update_queue_vis_append'][2]}")
            request.app['ws_requests']['update_queue_vis_append'][0] = False

        # Sending request for redundant token's list rewrite (on client side ofc)
        if request.app['ws_requests']['redundant_tokens_vis'][0]:
            for _ws in request.app['ws_list']:
                await _ws.send_str('update-redtokens ' + ''.join(token + ' ' for token in request.app['ws_requests']['redundant_tokens_vis'][1]))
            request.app['ws_requests']['redundant_tokens_vis'][0] = False
        await asyncio.sleep(0.1, loop=loop)
    async for msg in ws:
        if msg.type == web.WSMsgType.text:
            if msg.data == 'close':
                await ws.close()
    request.app['ws_list'].remove(ws)
    # loop = request.app.loop
    # while True:
    #     # Sending request for queue' token remove when it's been removed on server.
    #     if request.app['ws_requests']['update_queue_vis_remove']:
    #         for ws in request.app['ws_list']:
    #             await ws.send_str("update-remove")
    #         request.app['ws_requests']['update_queue_vis_remove'] = False
    #
    #     # Sending request for queue' token adding up when it's been added on server.
    #     if request.app['ws_requests']['update_queue_vis_append'][0]:
    #         for ws in request.app['ws_list']:
    #             await ws.send_str(f"update-append {request.app['ws_requests']['update_queue_vis_append'][1]} {request.app['ws_requests']['update_queue_vis_append'][2]}")
    #         request.app['ws_requests']['update_queue_vis_append'][0] = False
    #
    #     # Sending request for redundant token's list rewrite (on client side ofc)
    #     if request.app['ws_requests']['redundant_tokens_vis'][0]:
    #         for ws in request.app['ws_list']:
    #             await ws.send_str('update-redtokens ' + ''.join(token + ' ' for token in request.app['ws_requests']['redundant_tokens_vis'][1]))
    #         request.app['ws_requests']['redundant_tokens_vis'][0] = False
    #
    #     await asyncio.sleep(0.1, loop=loop)

    return ws

