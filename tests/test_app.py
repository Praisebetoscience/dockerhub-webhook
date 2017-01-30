"""Dockerhub-Webhook integration tests """
# pylint: disable=C0111,C0103,W0201,E0213
import json
import pytest
from test_base import BaseFlaskTester, post_mock, call_mock, recusive_del_key


class TestFlask(BaseFlaskTester):

    def test_index(self):
        rv = self.app.get('/')
        assert b'prodigiously empty' in rv.data

    def test_hubhook(self, mocker, post_mock, call_mock):

        url = '/hubhook?key={key}'.format(key='filesecret')
        rv = self.app.post(url,
                           data=json.dumps(self.default_payload),
                           content_type='application/json')

        assert b'deployed.' in rv.data

    @pytest.mark.parametrize('apikey, delkey, code, desc', [
        ('badkey', None, 403, 'Invalid API key'),
        ('filesecret', 'no payload', 400, 'Missing payload'),
        ('filesecret', 'callback_url', 400, 'payload.callback_url'),
        ('filesecret', 'repository', 400, 'payload.repository'),
        ('filesecret', 'name', 400, 'repository.name'),
        ('filesecret', None, 400, 'Hook for badhook not found')])
    def test_hubhook_errors(
            self, post_mock, call_mock, apikey, delkey, code, desc):
        data = None
        if delkey != 'no payload':
            payload = self.default_payload.copy()
            payload['repository']['name'] = 'badhook'
            recusive_del_key(payload, delkey)
            data = json.dumps(payload)
        url = '/hubhook?key={key}'.format(key=apikey)

        resp = self.app.post(url, data=data, content_type='application/json')
        response = json.loads(str(resp.data, 'utf8'))

        assert resp.status_code == code
        assert resp.content_type == 'application/json'
        assert response['state'] == 'error'
        assert desc in response['description']

        if delkey in ['no payload', 'callback_url']:
            assert not post_mock.called
        else:
            post_mock.assert_called_once_with(payload['callback_url'],
                                              json=response)

        assert not call_mock.called
