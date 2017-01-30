"""Base class that configures the dockerhook app for testing"""
# pylint: disable=C0111,C0103,W0201,E0213
import contextlib
import json
import os
import pytest
import dockerhook
from dockerhook.util import get_app_base_path


def recusive_del_key(dic: dict, key: str):
    """
    Recusively remove keys in a dictionary.

    >>> recusive_del_key({'a': 2, 'b': 1}, 'a')
    {'b': 1}

    >>> recusive_del_key({'b': 1}, None)
    {'b': 1}

    >>> recusive_del_key({'b': 1}, 'c')
    {'b': 1}

    >>> recusive_del_key({'b': {'a': 1, 'c': 4}}, 'c')
    {'b': {'a': 1}}

    :type dic: dict[str, unicode]
    :param dic: dictionary to remove key
    :type key: str
    :param key: key to remove
    """
    if not key:
        return dic

    dic.pop(key, None)
    for k in dic:
        if isinstance(dic[k], dict):
            recusive_del_key(dic[k], key)
    return dic


@contextlib.contextmanager
def set_env(**environ):
    """
    Temporarily set the process environment variables.

    >>> with set_env(PLUGINS_DIR=u'test/plugins'):
    ...   "PLUGINS_DIR" in os.environ
    True

    >>> with set_env(PLUGINS_DIR=None):
    ...   "PLUGINS_DIR" in os.environ
    False

    >>> "PLUGINS_DIR" in os.environ
    False

    :type environ: dict[str, unicode]
    :param environ: Environment variables to set
    """
    strip_environ = dict((k, v) for k, v in environ.items() if v is not None)
    old_environ = dict(os.environ)
    os.environ.update(strip_environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_environ)


@pytest.fixture
def post_mock(mocker):
    return mocker.patch('requests.post')


@pytest.fixture
def call_mock(mocker):
    call = mocker.patch('subprocess.call')
    call.return_value = 0
    return call


class BaseFlaskTester:

    def setup_class(cls):
        base_path = os.path.dirname(get_app_base_path())
        payload_file = os.path.join(base_path, 'tests/data/dockerhub.json')
        cls.default_payload = json.load(open(payload_file))
        cls.test_config_path = os.path.join(base_path, 'tests/data/config.py')

    def setup(self):
        with set_env(
                DOCKERHOOK_SETTINGS=self.test_config_path,
                FLASK_CONFIGURATION='testing'):

            dockerhook.app.config.from_envvar('DOCKERHOOK_SETTINGS')
            self.app = dockerhook.app.test_client()
