import logging
import subprocess
import requests
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
    def handler(cls, params, json_data):
        err = None

        if not params or params.get('key') != cls.cfg['apikey']:
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
            res = cls.create_response('error', err[0], err[1])
            if json_data:
                cls.callback(res, json_data.get('callback_url'))
            logging.error('Bad Request: %s', err[1])
            return res

        return cls.run_script(json_data)

    @classmethod
    def run_script(cls, json_data):
        hook = json_data['repository']['name']

        logging.debug("Payload from dockerhub")
        logging.debug(json_data)
        logging.info("Running hook on repo: %s", hook)

        error = subprocess.call(cls.cfg['hooks'][hook].split())
        if error:
            res = cls.create_response('error',
                                      '500',
                                      '{} failed.'.format(hook))
            logging.error('Error running script: %s', cls.cfg['hooks'][hook])
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
        res = requests.post(callback_url, json=res)

        logging.debug("Callback response:")
        logging.debug(res)
