#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

async def run_process(*cmd):
    '''
        Execute shell commands
    '''
    proc = await asyncio.create_subprocess_shell(*cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
        )
    data = await proc.stdout.read()
    line = data.decode('utf-8').rstrip('\n')
    await proc.wait()
    return line
