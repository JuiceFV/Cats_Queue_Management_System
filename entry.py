"""
asyncio - standard package for async programming since python3.4
argparse - package for the parsing arguments from cmd/terminal
aiohttp - package for the async web-programming <pip install aiohttp>
"""
import asyncio
import argparse
from aiohttp import web
from application import create_app
from application.settings import load_config


# Makes an effort to import the uvloop for the performance augment.
# Windows doesn't maintain the uvloop, so far. Therefore we throws the  Exception.
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print("Uvloop library doesn't available.")


# Sets the argument parser up
# 1) --host HOST which will be listened
# 2) --port PORT to accept connection
# 3) --config YOUR_CFG.yaml pass your own config for this project. The default settings are places at config.yaml
parser = argparse.ArgumentParser(description="Kitty Getter Project")
parser.add_argument('--host', help="Host to listen", default='0.0.0.0')
parser.add_argument('--port', help="Port to accept connection", default=8080)
parser.add_argument('-c', '--config', type=argparse.FileType('r'), help="Path to configuration file")
args = parser.parse_args()

# Creates an application.
# The function create_app() is located at app.py
app = create_app(config=load_config(args.config))

if __name__ == '__main__':
    web.run_app(app, host=args.host, port=args.port)
