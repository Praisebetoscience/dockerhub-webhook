"""Dockerhub-Webhook integration tests """
# pylint: disable=C0111,C0103,W0201,E0213
import copy
import json
import pytest
from test_base import BaseFlaskTester, post_mock, call_mock, recusive_del_key


class TestFlask(BaseFlaskTester):

    def test_index(self):
        rv = self.app.get('/')
        assert b'prodigiously empty' in rv.data

    def test_hubhook(self, post_mock, call_mock):

        url = '/hubhook?key={key}'.format(key='filesecret')
        rv = self.app.post(url,
                           data=json.dumps(self.default_payload),
                           content_type='application/json')

        assert b'deployed.' in rv.data

    @pytest.mark.parametrize('apikey, delkey, code, desc, fail_run', [
        ('badkey', None, 403, 'Invalid API key', False),
        ('filesecret', 'no payload', 400, 'Missing payload', False),
        ('filesecret', 'callback_url', 400, 'payload.callback_url', False),
        ('filesecret', 'repository', 400, 'payload.repository', False),
        ('filesecret', 'name', 400, 'repository.name', False),
        ('filesecret', None, 400, 'Hook for badhook not found', False),
        ('filesecret', None, 500, 'testpush failed', True)])
    def test_hubhook_errors(
            self, post_mock, call_mock, apikey, delkey, code, desc, fail_run):
        data = None
        if delkey != 'no payload':
            payload = copy.deepcopy(self.default_payload)
            if not fail_run:
                payload['repository']['name'] = 'badhook'
            recusive_del_key(payload, delkey)
            data = json.dumps(payload)
        url = '/hubhook?key={key}'.format(key=apikey)

        if fail_run:
            call_mock.return_value = 1

        resp = self.app.post(url, data=data, content_type='application/json')
        response = json.loads(str(resp.data, 'utf8'))

        assert desc in response['description']
        assert resp.status_code == code
        assert resp.content_type == 'application/json'
        assert response['state'] == 'error'

        if delkey in ['no payload', 'callback_url']:
            assert not post_mock.called
        else:
            post_mock.assert_called_once_with(payload['callback_url'],
                                              json=response)

        if not fail_run:
            assert not call_mock.called
        else:
            call_mock.assert_called_once_with(['scripts/test.sh'])
