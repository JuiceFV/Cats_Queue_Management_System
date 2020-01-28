import argparse
import asyncio
from aiohttp import web
from application import create_app

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print("Uvloop library doesn't available.")

parser = argparse.ArgumentParser(description="Kitty Getter Project")
parser.add_argument('--host', help="Host to listen", default='0.0.0.0')
parser.add_argument('--port', help="Port to accept connection", default=8080)

args = parser.parse_args()

app = create_app()

if __name__ == '__main__':
    web.run_app(app, host=args.host, port=args.port)
