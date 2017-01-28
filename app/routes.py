from app import app

from flask import request, jsonify, make_response
from .handler import DockerhubWebhook
DockerhubWebhook.config(open('config.json', 'r'))


@app.route("/")
def index():
    body = 'This is already so prodigiously empty that there' \
        'is nothing in it to clear away.\n'
    return body


@app.route('/hubhook', methods=['GET', 'POST'])
def hubhook():
    """
    Dockerhub Webhook handler.

    Returns:
        Request: Success/Failure of the handler.
    """
    res = DockerhubWebhook.handler(request.args, request.json)
    status_code = res.pop('status_code')
    return make_response(jsonify(res), status_code)


@app.route('/request', methods=['GET', 'POST'])
def req():
    from pprint import pprint
    pprint(dict(request.args))
    pprint(request.json)
    print(DockerhubWebhook.cfg['apikey'])

    return "done.\n"
