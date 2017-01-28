# -*- coding: utf-8 -*-
# pylint: disable=C0413, C0103

"""
wsgi front end for the webhook handler.
"""

__author__ = 'PraiseBeToScience'
__version__ = '0.2'
__license__ = 'MIT'

import logging
from flask import Flask

app = Flask(__name__)
from app import routes


# Setup Logging
@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)
    else:
        app.logger.setLevel(logging.DEBUG)
