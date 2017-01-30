# -*- coding: utf-8 -*-
# pylint: disable=C0413, C0103

__author__ = 'PraiseBeToScience'
__copyright__ = 'Copyright 2017 PraiseBeToScience'
__credits__ = ['PraiseBeToScience']
__license__ = 'Apache License 2.0'
__version__ = '0.2'
__maintainer__ = 'PraiseBeToScience'
__email__ = 'pbts.reddit@gmail.com'
__status__ = '5 - Production'


from flask import Flask, request, jsonify, make_response
from dockerhook.handler import DockerhubWebhook
from dockerhook.config import configure_app
from dockerhook.util import get_instance_folder_path


app = Flask(__name__,
            instance_path=get_instance_folder_path(),
            instance_relative_config=True)

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
