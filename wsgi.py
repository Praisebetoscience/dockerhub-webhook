#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103

"""
wsgi front end for the webhook listener.  Based on Bottle using gunicorn
server.
"""

__author__ = 'PraiseBeToScience'
__version__ = '0.1'
__license__ = 'MIT'

import logging

import bottle
from bottle import request, route, run, Response

from dochook import DockerhubWebhook

logger = logging.getLogger('dochook')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.debug('testing debug output')

DockerhubWebhook.config(open('config.json', 'r'))


@route("/")
def index():
    body = 'This is already so prodigiously empty that there' \
        'is nothing in it to clear away.\n'
    return Response(body)


@route('/hubhook', method=['post'])
def hubhook():
    """
    Dockerhub Webhook handler.

    Returns:
        Request: Success/Failure of the handler.
    """
    params = dict(request.params)
    json_data = request.json
    res = DockerhubWebhook.handler(params, json_data)

    return Response(res['description'], int(res['status_code']))



if __name__ == "__main__":
    run(host='0.0.0.0',
        port='5000',
        server='gunicorn',
        debug=True,
        reloader=True,
        workers=1)

app = bottle.default_app()
