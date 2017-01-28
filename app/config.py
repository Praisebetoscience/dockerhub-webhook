import json
import logging
from os import environ

from app import app

class Config(object):

    defaults = {'apikey': 'secret',
                'hooks': {'testpush': 'scripts/test.sh'}
               }

    def __init__(self, cfg_file=None):
        self.cfg = self.defaults.copy()

        if cfg_file:
            app.logger.debug('loading config from file...')
            local_cfg = json.load(cfg_file)
            cfg_file.close()
            for key in self.defaults:
                self.cfg[key] = local_cfg.get(key, self.cfg[key])

        if environ.get('DOCHOOK_TOKEN'):
            app.logger.debug("Token set from envionment varialbe")
            self.cfg['apikey'] = environ['DOCHOOK_TOKEN']

        app.logger.info('Configuration loaded.')
        app.logger.debug('config: %s', self.cfg)


    def update(self, cfg_file):
        new_cfg = json.load(cfg_file)
        cfg_file.close()

        for key in self.defaults:
            self.cfg[key] = new_cfg.get(key, self.cfg[key])

        app.logger.info('Dochook configuration updated.')
        app.logger.debug('config: %s', self.cfg)

    def __getitem__(self, key):
        return self.cfg[key]

    def __contains__(self, key):
        return key in self.cfg
