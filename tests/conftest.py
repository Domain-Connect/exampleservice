import io
import os
import sys

import dns.resolver
import pytest
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ['APP_DOMAIN'] = 'exampleservice.test'
os.environ['APP_PROTOCOL'] = 'https'
os.environ['APP_IP'] = '192.0.2.1'
sys.path.insert(0, ROOT)


def pytest_configure(config):
    config.addinivalue_line('filterwarnings', 'error')


class Answer:
    def __init__(self, value):
        self.value = value
        self.strings = [value.encode('utf-8')]

    def __str__(self):
        return self.value


def fake_dns(records):
    # records: {(name, type): [value, ...]}; a missing name is NXDOMAIN
    def resolve(name, rdtype, *args, **kwargs):
        if (name, rdtype) not in records:
            raise dns.resolver.NXDOMAIN()
        return [Answer(value) for value in records[(name, rdtype)]]
    return resolve


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError('live network access in a test')
    monkeypatch.chdir(ROOT)
    monkeypatch.setattr(dns.resolver.Resolver, 'resolve', refuse)
    monkeypatch.setattr(requests, 'get', refuse)
    monkeypatch.setattr(requests, 'post', refuse)


@pytest.fixture
def dns_records(monkeypatch):
    def install(records):
        monkeypatch.setattr(dns.resolver, 'resolve', fake_dns(records))
    return install


def wsgi_get(app, path, host, scheme='https'):
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': path,
        'QUERY_STRING': '',
        'SERVER_NAME': host.split(':')[0],
        'SERVER_PORT': '443' if scheme == 'https' else '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'HTTP_HOST': host,
        'wsgi.url_scheme': scheme,
        'wsgi.input': io.BytesIO(),
        'wsgi.errors': io.StringIO(),
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    result = {}

    def start_response(status, headers, exc_info=None):
        result['status'] = int(status.split()[0])
        result['headers'] = dict(headers)

    body = b''.join(app(environ, start_response))
    result['body'] = body.decode('utf-8')
    return result
