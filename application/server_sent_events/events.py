import asyncio
from aiohttp_sse import sse_response


async def send_request_for_queue_update(request):
    loop = request.app.loop
    async with sse_response(request) as resp:
        while True:
            if request.app['update_queue_vis']:
                await resp.send("update")
                request.app['update_queue_vis'] = False
            await asyncio.sleep(1, loop=loop)
    return resp


