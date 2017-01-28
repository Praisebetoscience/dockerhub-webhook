import subprocess
import requests

from app import app
from .config import Config

class DockerhubWebhook(object):

    cfg = Config()

    @classmethod
    def config(cls, cfg_file):
        cls.cfg.update(cfg_file)

    @staticmethod
    def create_response(state, status_code, description):
        return {'state': state,
                'description': description,
                'status_code': status_code}

    @classmethod
    def handler(cls, args, json_data):
        err = None

        if not args or args.get('key') != cls.cfg['apikey']:
            err = ('403', 'Invalid API key.')
        elif not json_data:
            err = ('400', 'Missing payload.')
        elif json_data.get('callback_url') is None:
            err = ('400', 'Missing payload.callback_url.')
        elif json_data.get('repository') is None:
            err = ('400', 'Missing payload.repository.')
        elif json_data['repository'].get('name') is None:
            err = ('400', 'Missing payload.repository.name.')
        elif json_data['repository']['name'] not in cls.cfg['hooks']:
            name = json_data['repository']['name']
            err = ('400', 'Hook for {} not found.'.format(name))

        if err:
            app.logger.error('Bad Request: %s', err[1])
            res = cls.create_response('error', err[0], err[1])
            if json_data:
                cls.callback(res, json_data.get('callback_url'))
            return res

        return cls.run_script(json_data)

    @classmethod
    def run_script(cls, json_data):
        hook = json_data['repository']['name']

        app.logger.debug("Payload from dockerhub:")
        app.logger.debug(json_data)
        app.logger.info("Running hook on repo: %s", hook)

        error = subprocess.call(cls.cfg['hooks'][hook].split())
        if error:
            res = cls.create_response('error',
                                      '500',
                                      '{} failed.'.format(hook))
            app.logger.error('Error running script: %s', cls.cfg['hooks'][hook])
        else:
            res = cls.create_response('success',
                                      '200',
                                      '{} deployed.'.format(hook))
        cls.callback(res, json_data['callback_url'])
        return res

    @classmethod
    def callback(cls, res: dict, callback_url: str):
        if not callback_url:
            return None
        payload = res.copy()
        payload.pop('status_code')
        dockerhub_response = requests.post(callback_url, json=payload)

        app.logger.debug("Callback response:")
        app.logger.debug(dockerhub_response.text)
