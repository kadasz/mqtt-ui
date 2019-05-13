#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import jinja2
import asyncio
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
    app.router.add_route('*', '/login', login, name='login')
    app.router.add_route('*', '/logout', logout, name='logout')
    app.router.add_static('/static', STATIC_DIR, name='static')
    return app

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app())
    web.run_app(app, access_log=logger, access_log_format=ACCESS_LOG_FORMAT, host='0.0.0.0', port='8383')

