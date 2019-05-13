#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from settings import ht
from aiohttp_security.abc import AbstractAuthorizationPolicy

class HTAuthorizationPolicy(AbstractAuthorizationPolicy):

    async def authorized_userid(self, identity):
        user = ht.users()[0]
        if user == identity:
            return identity
        return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False
        return True
