import asyncio
from aiohttp_sse import sse_response


async def sse_updates(request):
    loop = request.app.loop
    async with sse_response(request) as resp:
        while True:
            if request.app['sse_requests']['update_queue_vis_remove']:
                await resp.send("update-remove")
                request.app['sse_requests']['update_queue_vis_remove'] = False

            if request.app['sse_requests']['update_queue_vis_append'][0]:
                await resp.send(f"update-append {request.app['sse_requests']['update_queue_vis_append'][1]} {request.app['sse_requests']['update_queue_vis_append'][2]}")
                request.app['sse_requests']['update_queue_vis_append'][0] = False

            if request.app['sse_requests']['redundant_tokens_vis'][0]:
                await resp.send('update-redtokens ' + ''.join(token + ' ' for token in request.app['sse_requests']['redundant_tokens_vis'][1]))
                request.app['sse_requests']['redundant_tokens_vis'][0] = False

            await asyncio.sleep(0.1, loop=loop)
    return resp

