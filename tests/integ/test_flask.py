"""Dockerhub-Webhook integration tests """
import json

import dockerhook


class TestFlask:

    def setup(self):
        dockerhook.app.config['TESTING'] = True
        self.app = dockerhook.app.test_client()

    # def setup_class(self):
    #     with open('config.py', )

    def test_index(self):
        rv = self.app.get('/')
        assert b'prodigiously empty' in rv.data

    def test_hubhook(self):
        data = json.load(open('tests/data/dockerhub.json'))

        args = {'key': 'badkey'}

        rv = self.app.post('/hubhook?key=badkey',
                           data=json.dumps(data),
                           content_type='application/json')

        assert b'Invalid API key.' in rv.data
