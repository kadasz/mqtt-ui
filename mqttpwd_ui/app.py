#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import jinja2
import asyncio
import aiohttp_jinja2
from aiohttp import web
from cryptography import fernet
from aiohttp_session import get_session, session_middleware, setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from settings import NAME, TEMPLATE_DIR, STATIC_DIR, BASE_DIR, logger, ACCESS_LOG_FORMAT

@aiohttp_jinja2.template('index.html')
async def index(request):
    return {'title': NAME}

@aiohttp_jinja2.template('register.html')
async def register(request):
    return {'title': NAME}

async def create_app():
    app = web.Application()
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key, max_age=86400))
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
        context_processors=[aiohttp_jinja2.request_processor],)
    app.router.add_route('GET', '/', index, name='index')
    app.router.add_route('*', '/register', register, name='register')
    return app

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app())
    web.run_app(app, access_log=logger, access_log_format=ACCESS_LOG_FORMAT, host='0.0.0.0', port='8383')

