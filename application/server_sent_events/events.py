import asyncio
from aiohttp_sse import sse_response


async def sse_updates(request):
    loop = request.app.loop
    async with sse_response(request) as resp:
        while True:
            if request.app['request_for_queue_update_vis']:
                await resp.send("update")
                request.app['request_for_queue_update_vis'] = False
            if request.app['redundant_tokens_vis'][0]:
                await resp.send(''.join(token + ' ' for token in request.app['redundant_tokens_vis'][1]))
                request.app['redundant_tokens_vis'][0] = False
            await asyncio.sleep(1, loop=loop)
    return resp

