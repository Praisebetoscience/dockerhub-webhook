# -*- coding: utf-8 -*-
# pylint: disable=C0413, C0103

__author__ = 'PraiseBeToScience'
__version__ = '0.2'
__license__ = 'MIT'


from flask import Flask, request, jsonify, make_response
from dockerhook.handler import DockerhubWebhook
from dockerhook.config import configure_app
from dockerhook.util import get_instance_folder_path


app = Flask(__name__,
            instance_path=get_instance_folder_path(),
            instance_relative_config=True,)

configure_app(app)

print(get_instance_folder_path())


@app.route("/")
def index():
    body = 'This is already so prodigiously empty that there' \
        ' is nothing in it to clear away.\n'
    return body


@app.route('/hubhook', methods=['GET', 'POST'])
def hubhook():
    """
    Dockerhub Webhook handler.

    Returns:
        Request: Success/Failure of the handler.
    """
    res = DockerhubWebhook.handler(request)
    status_code = res.pop('status_code')
    return make_response(jsonify(res), status_code)
