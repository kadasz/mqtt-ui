#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import aiohttp_jinja2
from settings import NAME, ht
from utils import run_process
from aiohttp.web  import Response, HTTPFound, json_response
from aiohttp_security import remember, forget, authorized_userid


async def validate_login(form):
    error = None

    username = form['username']
    password = form['password']

    cur_user = ht.users()
    if not username in cur_user:
        ht.set_password(username, password)
        ht.save()
        error = None
    if username in cur_user and not ht.check_password(username, password):
        error = 'Not valid password'
    return dict(error=error, user=f'{cur_user[0]}' if cur_user else username)


def redirect(router, route_name):
    location = router[route_name].url_for()
    return HTTPFound(location)

@aiohttp_jinja2.template('index.html')
async def index(request):
    auth = await authorized_userid(request)
    if not auth:
        if not ht.users():
            request.app['register'] = 'register'
            raise redirect(request.app.router, 'login')
        elif 'admin' in ht.users():
            request.app['register'] = None
            raise redirect(request.app.router, 'login')
    else:
        return {'title': NAME,  'username': auth}

async def logout(request):
    response = redirect(request.app.router, 'login')
    await forget(request, response)
    return response

@aiohttp_jinja2.template('login.html')
async def login(request):
    if request.method == 'POST':
        form = await request.post()
        is_validate = await validate_login(form)
        if is_validate.get('error'):
            return {'error': is_validate.get('error')}
        else:
            user = is_validate.get('user')
            response = redirect(request.app.router, 'index')
            request['user'] = user
            await remember(request, response, user)
            raise response

async def uptime(request):
    auth = await authorized_userid(request)
    if not auth:
        raise redirect(request.app.router, 'login')
    elif auth:
        data = await run_process('uptime')
        return Response(text=data)

async def pwdchange(request):
    auth = await authorized_userid(request)
    if not auth:
        raise redirect(request.app.router, 'login')
    elif auth :
        data = await request.json()
        newpass = data.get('pwd', None)
        if newpass:
            ht.set_password("admin", newpass)
            ht.save()
            return json_response({'Admin password has changed': 'success'})
