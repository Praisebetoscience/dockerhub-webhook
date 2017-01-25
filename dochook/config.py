import logging
import json
from os import environ


class Config(object):

    defaults = {'apikey': 'secret',
                'hooks': {'testpush': 'scripts/test.sh'}
               }

    def __init__(self, cfg_file=None):
        self.cfg = self.defaults

        if cfg_file:
            local_cfg = json.load(cfg_file)
            cfg_file.close()
            for k, val in local_cfg.items():
                if k in self.cfg:
                    self.cfg[k] = val

        self.cfg['apikey'] = environ.get('DOCHOOK_TOKEN', self.cfg['apikey'])
        logging.debug('DockerhubWebhook configuration loaded:')
        logging.debug(self.cfg)


    def update(self, cfg_file):
        new_cfg = json.load(cfg_file)
        cfg_file.close()

        for k, val in new_cfg.items():
            if k in self.cfg:
                self.cfg[k] = val

        logging.debug('DockerhubWebhook configuration updated:')
        logging.debug(self.cfg)

    def __getitem__(self, key):
        return self.cfg[key]

    def __contains__(self, key):
        return key in self.cfg
