import os
from flask import Flask
import pytest
from dockerhook.config import configure_app
from dockerhook.util import get_app_base_path

from test_base import set_env


@pytest.mark.parametrize(
    'envtoken, flask_conf, test_path, apikey, debug, testing', [
        (None, 'default', 'missing', 'secret', False, False),
        (None, 'development', 'missing', 'secret', True, True),
        (None, 'testing', 'missing', 'secret', False, True),
        (None, None, '../tests/data', 'filesecret', False, False),
        ('envsecret', None, '../tests/data/', 'envsecret', False, False)])
def test_config_app(envtoken, flask_conf, test_path, apikey, debug, testing):
    base_path = get_app_base_path()
    instance_path = os.path.join(base_path, test_path)

    with set_env(DOCKERHOOK_TOKEN=envtoken, FLASK_CONFIGURATION=flask_conf):
        app = Flask(__name__,
                    instance_path=instance_path,
                    instance_relative_config=True)

        configure_app(app)

    assert app.config['APIKEY'] == apikey
    assert app.config['DEBUG'] == debug
    assert app.config['TESTING'] == testing
