import requests

import util


class Response:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data


def test_valid_hostnames():
    assert util.is_valid_hostname('example.com')
    assert util.is_valid_hostname('sub-1.example.com.')
    assert not util.is_valid_hostname('a.b')
    assert not util.is_valid_hostname('-a.example.com')
    assert not util.is_valid_hostname('a_b.example.com')


def test_valid_messages():
    assert util.is_valid_message('Hello, world 1?!')
    assert not util.is_valid_message('')
    assert not util.is_valid_message('<b>')


def test_message_txt_value():
    assert util.dns_message_data('Hi').startswith('shm:')
    assert util.dns_message_data('Hi').endswith(':Hi')


def test_legacy_message_without_timestamp(dns_records):
    dns_records({('example.com', 'TXT'): ['shm:legacy']})
    assert util.get_messagetext('example.com') == 'legacy<br>'


def test_discovery_reads_settings(dns_records, monkeypatch):
    dns_records({
        ('_domainconnect.example.com', 'TXT'): ['api.provider.test'],
        ('example.com', 'NS'): ['ns1.provider.test.'],
    })
    settings = {'providerName': 'Provider', 'nameServers': ['ns1.provider.test']}
    urls = []

    def get(url, **kwargs):
        urls.append(url)
        return Response(200, settings)
    monkeypatch.setattr(requests, 'get', get)

    assert util.get_domainconnect_json('example.com') == (settings, 'api.provider.test', None)
    assert urls == ['https://api.provider.test/v2/example.com/settings']


def test_discovery_rejects_other_name_servers(dns_records, monkeypatch):
    dns_records({
        ('_domainconnect.example.com', 'TXT'): ['api.provider.test'],
        ('example.com', 'NS'): ['ns1.other.test.'],
    })
    monkeypatch.setattr(requests, 'get', lambda url, **kwargs: Response(200, {'nameServers': ['ns1.provider.test']}))

    assert util.get_domainconnect_json('example.com') == (None, None, 'Nameservers not authoritative')


def test_discovery_without_record(dns_records):
    dns_records({})
    assert util.get_domainconnect_json('example.com') == (None, None, 'Internal error')
