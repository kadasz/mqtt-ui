#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import jinja2
import asyncio
import argparse
from views import *
import aiohttp_jinja2
from aiohttp import web
from cryptography import fernet
from auth import HTAuthorizationPolicy
from aiohttp_security import SessionIdentityPolicy
from aiohttp_session import setup as setup_session
from aiohttp_security import SessionIdentityPolicy
from aiohttp_security import setup as setup_security
from aiohttp_session import get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from settings import NAME, TEMPLATE_DIR, STATIC_DIR, BASE_DIR, logger, ACCESS_LOG_FORMAT

async def create_app():
    app = web.Application()
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup_session(app, EncryptedCookieStorage(secret_key, max_age=86400))
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
        context_processors=[aiohttp_jinja2.request_processor],)
    setup_security(app, SessionIdentityPolicy(), HTAuthorizationPolicy())
    app.router.add_route('GET', '/', index, name='index')
    app.router.add_route('GET', '/api/uptime', uptime, name='uptime')
    app.router.add_route('POST', '/api/pwdchange', pwdchange, name='pwdchange')
    app.router.add_route('*', '/login', login, name='login')
    app.router.add_route('*', '/logout', logout, name='logout')
    app.router.add_static('/static', STATIC_DIR, name='static')
    return app

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="mqttUI server start")
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Set the bind address for mqttUI (default: %(default)s)')
    parser.add_argument('--port', type=int, default=8383, help='Set listen on a specified port (default: %(default)s)')
    parser.add_argument('--pwd', type=str, help='Select path to the mosquitto password file')
    args = parser.parse_args()
    if not args.pwd:
        parser.error("--pwd requires. Please specify path to the mosquitto password file")
        parser.exit()
    elif args.pwd:
        pass
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app())
    app['pwd'] = args.pwd
    web.run_app(app, access_log=logger, access_log_format=ACCESS_LOG_FORMAT, host=args.host, port=args.port)

