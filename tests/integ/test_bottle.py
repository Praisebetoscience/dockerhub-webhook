""" dochook bottle integration tests """
from io import StringIO
import json
from boddle import boddle
from wsgi import index, hubhook
from dochook import DockerhubWebhook


def test_index():
    with boddle(method='get'):
        assert 'prodigiously empty' in index().body


def test_hubhook():
    config = json.load(open('tests/data/config.json'))
    body = json.load(open('tests/data/dockerhub.json'))
    DockerhubWebhook.config(StringIO(json.dumps(config)))

    params = {'key': 'badkey'}

    with boddle(method='post', params=params, json=body,):
        assert 'Invalid API' in hubhook().body
