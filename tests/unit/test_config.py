from app.handler import DockerhubWebhook
from app.config import Config


def test_default():
    cfg = Config()
    assert cfg['apikey'] == "secret"


def test_config_with_file():
    cfg = Config(open('tests/data/config.json', 'r'))
    assert cfg['apikey'] == "testsecret"
    assert 'badkey' not in cfg


def test_config_with_env(monkeypatch):
    monkeypatch.setenv("DOCHOOK_TOKEN", 'envsecret')
    cfg = Config(open('tests/data/config.json', 'r'))
    assert cfg['apikey'] == "envsecret"


def test_update_method():
    cfg = Config()
    cfg.update(open('tests/data/config.json'))
    assert cfg['apikey'] == 'testsecret'


def test_class_config_method():
    DockerhubWebhook.config(open('tests/data/config.json', 'r'))
    assert DockerhubWebhook.cfg['apikey'] == 'testsecret'
