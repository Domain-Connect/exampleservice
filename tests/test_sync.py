import statelesshosting
from conftest import wsgi_get, wsgi_post

HOST = 'exampleservice.test'
SETTINGS = {'providerName': 'Provider', 'urlAPI': 'https://api.provider.test', 'urlSyncUX': 'https://ux.provider.test',
            'nameServers': ['ns1.provider.test']}
FORM = {'domain': 'example.com', 'subdomain': 'www', 'message': 'Hi'}


def test_index_passes_dc_txt_on():
    r = wsgi_get(statelesshosting.app, '/sync_index', HOST, query='dc_txt=api.provider.test')
    assert "name='dc_txt' value='api.provider.test'" in r['body']


def test_post_with_dc_txt_uses_it_for_any_domain(dns_records, dns_provider):
    dns_records({})
    urls = dns_provider(SETTINGS)
    r = wsgi_post(statelesshosting.app, '/sync_post', HOST, dict(FORM, dc_txt='api.provider.test'))
    assert r['status'] == 200
    assert urls[0] == 'https://api.provider.test/v2/example.com/settings'
    assert 'https://ux.provider.test/v2/domainTemplates/providers/exampleservice.domainconnect.org/services/template2/apply?domain=example.com' in r['body']
    assert 'api.provider.test (dc_txt)' in r['body']


def test_post_with_invalid_dc_txt_is_invalid_data(dns_records, dns_provider):
    dns_records({})
    dns_provider(SETTINGS)
    r = wsgi_post(statelesshosting.app, '/sync_post', HOST, dict(FORM, dc_txt='<b>'))
    assert 'Invalid Data' in r['body']
