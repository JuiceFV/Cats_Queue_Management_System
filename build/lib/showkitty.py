import aiohttp_flashbag
from aiohttp import web, ClientSession
from aiohttp_session import setup as setup_session
from aiohttp_session import SimpleCookieStorage
from PIL import Image
import io
import asyncio

token_list = []


# async def cheater_hendle(request):
# ------------------------token_func------------------------------------
async def time_limit_out():
    while len(token_list) != 0:
        before = token_list[0]
        await asyncio.sleep(60)
        if len(token_list) != 0:
            if token_list[0] == before:
                token_list.pop(0)
            else:
                break
        else:
            break


def get_token():
    add_token()
    return token_list[-1]


def add_token():
    if (len(token_list) == 0):
        token_list.append(0)
    elif (token_list[-1] < 99):
        token_list.append(token_list[-1] + 1)
    else:
        token_list.append(0)


async def token_handler(request):
    token = str(get_token())
    aiohttp_flashbag.flashbag_set(request, 'number', token)
    if len(token_list) == 1 and token_list[0] == 0:
        asyncio.gather(time_limit_out())
    return web.HTTPSeeOther('/')


# ------------------------end_token_func---------------------------------
# ------------------------image_func-------------------------------------
url = 'https://api.thecatapi.com/v1/images/search'
headers = {
    'Content-Type': 'image/jpeg',
    'x-api-key': 'e3efb418-dd58-42a0-9b11-0bb34df8d574'
}


async def validate_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    return image.width >= 1024 and image.height >= 1024


async def get_cat_image_from_thecatapi():
    while True:
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                resp_dict = await resp.json()
        image_url = resp_dict[0]['url']
        return image_url


async def get_cat_image_byte():
    image_url = await get_cat_image_from_thecatapi()
    async with ClientSession() as session:
        async with session.get(image_url) as resp:
            image_bytes = await resp.read()
    return image_bytes


async def get_cat_image(request):
    image = await get_cat_image_byte()
    return web.Response(body=image, content_type='image/jpg')


# --------------------end_image_func-------------------------------------
async def handler_get(request):
    validation_error = aiohttp_flashbag.flashbag_get(request, 'error')
    validation_number = aiohttp_flashbag.flashbag_get(request, 'number')
    error_html = ''
    number_html = ''
    if validation_error is not None:
        error_html = '<span>{validation_error}</span>'.format(
            validation_error=validation_error,
        )

    if validation_number is not None:
        number_html = '<span>{validation_number}</span>'.format(
            validation_number=validation_number,
        )
    body = '''
            <html>
                <head><title>Show kitty</title></head>
                <body>
                <form method="GET" action="/get_token">
                        <input type="submit" value="Get number">
                        Your number is: {number_html}
                    </form>
                    <form method="POST" action="/">
                        <input type="text" name="token" />

                        <input type="submit" value="Show kitty">
                    </form>
                    {error_html}
                </body>
            </html>
        '''
    body = body.format(error_html=error_html, number_html=number_html)
    return web.Response(body=body.encode('utf-8'), content_type='text/html')


async def handler_post(request):
    post = await request.post()
    if len(post['token']) == 0:
        aiohttp_flashbag.flashbag_set(request, 'error', 'Input your token')
        return web.HTTPSeeOther('/')
    if (token_list.count(int(post['token'])) == 0):
        return web.StreamResponse(status=423, reason='CHEATING')#не осоюо понял, пусть буде так
    if post['token'] != str(token_list[0]):
        aiohttp_flashbag.flashbag_set(request, 'error', 'Try again later!')
        return web.HTTPSeeOther('/')

    token_list.pop(0)
    asyncio.gather(time_limit_out())
    return web.HTTPSeeOther('/cat')


def make_app():
    session_storage = SimpleCookieStorage()
    app = web.Application()
    setup_session(app, session_storage)
    app.middlewares.append(aiohttp_flashbag.flashbag_middleware)
    app.router.add_route(
        'GET',
        '/',
        handler_get,
    )
    app.router.add_route(
        'GET',
        '/cat',
        get_cat_image,
    )
    app.router.add_route(
        'GET',
        '/get_token',
        token_handler,
    )
    app.router.add_route(
        'POST',
        '/',
        handler_post,
    )
    return app


web.run_app(make_app())
