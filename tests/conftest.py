import io
import os
import sys
import urllib.parse

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


def wsgi_get(app, path, host, scheme='https', query=''):
    return wsgi_call(app, 'GET', path, host, scheme, query, b'')


def wsgi_post(app, path, host, form, scheme='https'):
    return wsgi_call(app, 'POST', path, host, scheme, '', urllib.parse.urlencode(form).encode('utf-8'))


def wsgi_call(app, method, path, host, scheme, query, body):
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': query,
        'CONTENT_TYPE': 'application/x-www-form-urlencoded',
        'CONTENT_LENGTH': str(len(body)),
        'SERVER_NAME': host.split(':')[0],
        'SERVER_PORT': '443' if scheme == 'https' else '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'HTTP_HOST': host,
        'wsgi.url_scheme': scheme,
        'wsgi.input': io.BytesIO(body),
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

    result['body'] = b''.join(app(environ, start_response)).decode('utf-8')
    return result


class Response:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data


@pytest.fixture
def dns_provider(monkeypatch):
    # Answers the settings of every domain and supports every template; returns the URLs requested
    def install(settings):
        urls = []

        def get(url, **kwargs):
            urls.append(url)
            if url.endswith('/settings'):
                return Response(200, settings)
            return Response(200)
        monkeypatch.setattr(requests, 'get', get)
        return urls
    return install
