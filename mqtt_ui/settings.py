#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging

NAME = 'mqttUI'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

LOG_FORMAT = "%(asctime)s %(name)s: [%(levelname)s] %(message)s"
LOG_DATE_FORMAT = "[ %Y-%m-%d %H:%M:%S ]"
ACCESS_LOG_FORMAT = f'anonymous@%a - %r %s %b %Tf'
logger = logging.getLogger(NAME)
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
console.setLevel(logging.DEBUG)
logger.addHandler(console)
