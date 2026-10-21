import statelesshosting
from conftest import wsgi_get, wsgi_post

HOST = 'exampleservice.test'
SETTINGS = {'providerName': 'GoDaddy', 'urlAPI': 'https://domainconnect.api.godaddy.com',
            'urlAsyncUX': 'https://ux.provider.test', 'nameServers': ['ns1.provider.test']}
FORM = {'domain': 'example.com', 'hosts': ''}


def test_index_passes_dc_txt_on():
    r = wsgi_get(statelesshosting.app, '/async_index', HOST, query='dc_txt=api.provider.test')
    assert "name='dc_txt' value='api.provider.test'" in r['body']


def test_post_with_dc_txt_uses_it_for_any_domain(dns_records, dns_provider):
    dns_records({})
    urls = dns_provider(SETTINGS)
    r = wsgi_post(statelesshosting.app, '/async_post', HOST, dict(FORM, dc_txt='api.provider.test'))
    assert r['status'] == 200
    assert urls[0] == 'https://api.provider.test/v2/example.com/settings'
    assert 'https://ux.provider.test/v2/domainTemplates/providers/exampleservice.domainconnect.org?domain=example.com' in r['body']
    assert 'api.provider.test (dc_txt)' in r['body']


def test_post_with_invalid_dc_txt_is_invalid_data(dns_records, dns_provider):
    dns_records({})
    dns_provider(SETTINGS)
    r = wsgi_post(statelesshosting.app, '/async_post', HOST, dict(FORM, dc_txt='api.provider.test:0'))
    assert 'Invalid Data' in r['body']


def test_index_passes_dc_proto_on():
    r = wsgi_get(statelesshosting.app, '/async_index', HOST, query='dc_proto=http')
    assert "name='dc_proto' value='http'" in r['body']


def test_post_with_dc_proto_calls_settings_over_it(dns_records, dns_provider):
    dns_records({})
    urls = dns_provider(SETTINGS)
    r = wsgi_post(statelesshosting.app, '/async_post', HOST, dict(FORM, dc_txt='api.provider.test', dc_proto='http'))
    assert r['status'] == 200
    assert urls[0] == 'http://api.provider.test/v2/example.com/settings'
    assert 'http://api.provider.test/v2/example.com/settings' in r['body']


def test_post_with_invalid_dc_proto_is_invalid_data(dns_records, dns_provider):
    dns_records({})
    dns_provider(SETTINGS)
    r = wsgi_post(statelesshosting.app, '/async_post', HOST, dict(FORM, dc_txt='api.provider.test', dc_proto='file'))
    assert 'Invalid Data' in r['body']
