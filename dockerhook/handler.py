"""Main handler class for dockerhub-webhook"""

# Built in imports
import subprocess

# Third party imports
import requests
from flask import current_app as app


class DockerhubWebhook(object):

    """
    Handler class for docker-webhook.  Validates requests, processes scripts,
    fetches callbacks, and responsds with status.
    """
    @staticmethod
    def create_response(state, status_code, description):
        """
        Helper function to create the JSON dict.

        Args:
            state (str): Dockerhub state
            status_code (str): HTTP status code
            description (str): Docker Hub description of result.

        Returns:
            dict: JSON reponse.
        """
        return {'state': state,
                'description': description,
                'status_code': status_code}

    @classmethod
    def handler(cls, request):
        """
        Main handler.  Validates incoming requests, then passes data to
        the callback and run_scipt process.

        Args:
            request (Flask.Request): Incoming request from Flask

        Returns:
            Dict: JSON response.
        """
        args = request.args
        json_data = request.get_json(silent=True)
        err = None

        app.logger.debug("Payload from dockerhub:")
        app.logger.debug(json_data)
        app.logger.info('Request from: %s', request.remote_addr)

        if not args or args.get('key') != app.config['APIKEY']:
            err = ('403', 'Invalid API key.')
        elif not json_data:
            err = ('400', 'Missing payload.')
        elif json_data.get('callback_url') is None:
            err = ('400', 'Missing payload.callback_url.')
        elif json_data.get('repository') is None:
            err = ('400', 'Missing payload.repository.')
        elif json_data['repository'].get('name') is None:
            err = ('400', 'Missing payload.repository.name.')
        elif json_data['repository']['name'] not in app.config['HOOKS']:
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
        """
        Shell command handler.  Runs docker update script from app.config.

        Args:
            json_data (dict): JSON payload from Docker Hub.

        Returns:
            Dict: JSON Response
        """
        hook = json_data['repository']['name']
        script = app.config['HOOKS'][hook]

        app.logger.info("Triggering hook on repo: %s", hook)

        error = subprocess.call(script.split())
        if error:
            res = cls.create_response('error',
                                      '500',
                                      '{} failed.'.format(hook))
            app.logger.error('Error running script: %s', script)
        else:
            res = cls.create_response('success',
                                      '200',
                                      '{} deployed.'.format(hook))
            app.logger.info('Script completed successfully.')
        cls.callback(res, json_data['callback_url'])
        return res

    @classmethod
    def callback(cls, res: dict, callback_url: str):
        """
        Callback Handler - issues callback to Docker Hub.

        Args:
            res (JSON): JSON response
            callback_url (str): callback url
        """
        if not callback_url:
            return None
        payload = res.copy()
        payload.pop('status_code')
        dockerhub_response = requests.post(callback_url, json=payload)

        app.logger.debug("Callback response:")
        app.logger.debug(dockerhub_response.text)
