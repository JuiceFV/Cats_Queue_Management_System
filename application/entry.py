"""The 'entry.py' is the entry point of the application.
In this file we declare the application and start its work.
Also, there are defined flags and options for the application.
"""


import asyncio
import argparse
from aiohttp import web
from application.sources import create_app
from application.sources.settings import load_config

# Makes an effort to import the uvloop for the performance augment.
# WindowsOS doesn't maintain the uvloop, so far. Therefore we throws the  Exception.
# Uvloop's GitHub: https://github.com/MagicStack/uvloop
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print("Uvloop library doesn't available.")


# Sets the argument parser up. For these purposes we're using 'argparse'-package (installation: pip install argparse)
# 1) --host HOST: the host which will be listened, the default host is '0.0.0.0'. (Ex: python entry.py --host 127.0.0.1)
# 2) --port PORT: the port to accept a connection, the default port is '8080'. (Ex: python entry.py --port 5432)
# 3) --config YOUR_CFG.yaml: pass your own config for the application. The default settings are places at config.yaml
#      If you'd like so, you can pass your own cfg-file. (Ex: python entry.py -c my_cfg.yaml).
#      You can use as same '--config' as '-c'.
# 4) --test: makes the run-type = test. Generally it do nothing merely changing the path to the static files in routes.
#      (Ex: python entry.py --test). You shouldn't pass an argument. The option 'action='store_true' makes it possible.
# 5) --debug: makes the run-type = debug. Hmm, this flag just turning debug-logging on. That's all.
#      (Ex: python entry.py -debug). I believe you're an ingenious man therefore you grasp why does it work
#      w/o arguments.
# 6) --release: makes the run-type = release. Removing debugging logs. (Ex: python entry.py --release).
#      Look up the line above.
parser = argparse.ArgumentParser(description="Kitty Getter Project")
parser.add_argument('--host', help="Host to listen", default='0.0.0.0')
parser.add_argument('--port', help="Port to accept connection", default=8080)
parser.add_argument('-c', '--config', type=argparse.FileType('r'), help="Path to configuration file")
parser.add_argument('--test', help="The run-type sets as test", action='store_true')
parser.add_argument('--debug', help="The run-type sets as debug", action='store_true')
parser.add_argument('--release', help="The run-type sets as release", action='store_true')
args = parser.parse_args()


def main():
    """The main function, which creates an application and launch it.
    """
    # Creates an application with already set configuration and routes.
    # The function create_app() is located at app.py
    config, is_test = load_config(args.config, args.test, args.debug, args.release)
    app = create_app(config=config)

    # Depending on test-argument - start the application or tests
    if not is_test:
        web.run_app(app, host=args.host, port=args.port)
    else:
        from application.tests import start_tests
        start_tests()


if __name__ == '__main__':
    main()
