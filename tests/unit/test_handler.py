import pytest
from app.handler import DockerhubWebhook


def pop_key(dic: dict, key: str):
    """
    Recusively pop 'key' from dict

    Args:
        dic (dict): Dictionary to traverse
        key (str): key to remove
    """
    dic.pop(key, None)
    for k in dic:
        if isinstance(dic[k], dict):
            pop_key(dic[k], key)


@pytest.fixture
def json_data():
    import json
    return json.load(open('tests/data/dockerhub.json'))


@pytest.fixture
def params():
    return {'key': 'testsecret'}


@pytest.fixture
def request_mock(mocker):
    return mocker.patch('requests.post')


@pytest.fixture
def config_dwh():
    DockerhubWebhook.config(open('tests/data/config.json'))
    return DockerhubWebhook


@pytest.fixture
def call_mock(mocker):
    call = mocker.patch('subprocess.call')
    call.return_value = 0
    return call


def test_success_push(config_dwh, request_mock, params, json_data, call_mock):
    res = DockerhubWebhook.handler(params, json_data)
    assert res['status_code'] == '200'
    assert 'deployed.' in res['description']
    assert res['state'] == 'success'

    res.pop('status_code')
    request_mock.assert_called_once_with(json_data['callback_url'],
                                         json=res)
    call_mock.assert_called_once_with(['scripts/test.sh'])


def test_script_error(config_dwh, request_mock, params, json_data, call_mock):
    call_mock.return_value = 1
    res = DockerhubWebhook.handler(params, json_data)
    assert res['status_code'] == '500'
    assert 'failed.' in res['description']
    assert res['state'] == 'error'

    res.pop('status_code')
    request_mock.assert_called_once_with(json_data['callback_url'],
                                         json=res)
    call_mock.assert_called_once_with(['scripts/test.sh'])



@pytest.mark.parametrize("params", [
    {'key': 'badkey'},
    {'key': ''},
    {},
    None])
def test_bad_api_key(json_data, request_mock, config_dwh, params):
    res = DockerhubWebhook.handler(params, json_data)

    assert res['status_code'] == '403'
    assert res['description'] == 'Invalid API key.'
    assert res['state'] == 'error'

    res.pop('status_code')
    request_mock.assert_called_once_with(json_data['callback_url'],
                                         json=res)


def test_no_json_data(request_mock, config_dwh, params):
    res = DockerhubWebhook.handler(params, None)

    assert res['status_code'] == '400'
    assert res['description'] == 'Missing payload.'
    assert res['state'] == 'error'

    request_mock.assert_not_called()


@pytest.mark.parametrize('missing_key, description', [
    ('repository', 'Missing payload.repository.'),
    ('callback_url', 'Missing payload.callback_url.'),
    ('name', 'Missing payload.repository.name.')
])
def test_missing_json_keys(request_mock, config_dwh, params, json_data,
                           missing_key, description):
    pop_key(json_data, missing_key)
    res = DockerhubWebhook.handler(params, json_data)

    assert res['status_code'] == '400'
    assert res['description'] == description
    assert res['state'] == 'error'

    if missing_key == 'callback_url':
        request_mock.assert_not_called()
    else:
        res.pop('status_code')
        request_mock.assert_called_once_with(json_data['callback_url'],
                                             json=res)


def test_missing_hook(request_mock, config_dwh, params, json_data):
    json_data['repository']['name'] = 'badhook'
    res = DockerhubWebhook.handler(params, json_data)

    assert res['status_code'] == '400'
    assert 'not found' in res['description']
    assert res['state'] == 'error'

    res.pop('status_code')
    request_mock.assert_called_once_with(json_data['callback_url'],
                                         json=res)
