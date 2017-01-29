import logging
import logging.handlers
import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    LOGGING_LOCATION = 'log/dockerhook.log'
    LOGGING_FORMAT = '[%(asctime)s] [%(levelname)s] %(message)s'
    LOGGING_DATEFMT = '%Y-%m-%d %H:%M:%S %z'
    LOGGING_LEVEL = logging.INFO
    APIKEY = 'secret'
    HOOKS = {'testpush': 'scripts/test.sh'}


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = logging.DEBUG


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True

config = {
    'development': 'dockerhook.config.DevelopmentConfig',
    'testing': 'dockerhook.config.TestingConfig',
    'default': 'dockerhook.config.BaseConfig'
}


def configure_app(app):
    config_name = os.environ.get('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py', silent=True)
    apikey = os.environ.get('DOCKERHUB_TOKEN', None)
    if apikey:
        app.config['APIKEY'] = apikey
    # Configure Logging
    handler = logging.handlers.RotatingFileHandler(
        app.config['LOGGING_LOCATION'], 'a', 1 * 1024 * 1024, 10, 'utf8')
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(
        app.config['LOGGING_FORMAT'], app.config['LOGGING_DATEFMT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(app.config['LOGGING_LEVEL'])

