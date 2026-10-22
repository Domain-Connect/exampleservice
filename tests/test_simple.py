import re
import urllib.parse

import statelesshosting
import sigutil
from test_sigutil import public_key_pem
from conftest import wsgi_get, wsgi_post

HOST = 'exampleservice.test'
SETTINGS = {'providerName': 'Provider', 'urlAPI': 'https://api.provider.test', 'urlSyncUX': 'https://ux.provider.test',
            'nameServers': ['ns1.provider.test']}
FORM = {'domain': 'example.com', 'subdomain': '', 'message': 'Hi'}


def test_index_passes_dc_txt_on():
    r = wsgi_get(statelesshosting.app, '/simple_index', HOST, query='dc_txt=api.provider.test%2F%22x')
    assert "name='dc_txt' value='api.provider.test/&quot;x'" in r['body']


def test_post_with_dc_txt_uses_it_for_any_domain(dns_records, dns_provider):
    dns_records({})
    urls = dns_provider(SETTINGS)
    r = wsgi_post(statelesshosting.app, '/simple_post', HOST, dict(FORM, dc_txt='api.provider.test'))
    assert r['status'] == 200
    assert urls[0] == 'https://api.provider.test/v2/example.com/settings'
    assert 'https://ux.provider.test/v2/domainTemplates/providers/exampleservice.domainconnect.org/services/template2/apply?domain=example.com' in r['body']
    assert '_domainconnect record: api.provider.test (dc_txt)' in r['body']


def test_post_with_invalid_dc_txt_is_invalid_data(dns_records, dns_provider):
    dns_records({})
    dns_provider(SETTINGS)
    r = wsgi_post(statelesshosting.app, '/simple_post', HOST, dict(FORM, dc_txt='api.provider.test?x'))
    assert 'Invalid Data' in r['body']


def test_index_passes_dc_proto_on():
    r = wsgi_get(statelesshosting.app, '/simple_index', HOST, query='dc_proto=http')
    assert "name='dc_proto' value='http'" in r['body']


def test_post_with_dc_proto_calls_settings_over_it(dns_records, dns_provider):
    dns_records({})
    urls = dns_provider(SETTINGS)
    r = wsgi_post(statelesshosting.app, '/simple_post', HOST, dict(FORM, dc_txt='api.provider.test:8443', dc_proto='http'))
    assert r['status'] == 200
    assert urls[0] == 'http://api.provider.test:8443/v2/example.com/settings'


def test_post_with_invalid_dc_proto_is_invalid_data(dns_records, dns_provider):
    dns_records({})
    dns_provider(SETTINGS)
    r = wsgi_post(statelesshosting.app, '/simple_post', HOST, dict(FORM, dc_txt='api.provider.test', dc_proto='ftp'))
    assert 'Invalid Data' in r['body']


def test_post_links_apply_url_with_redirect_in_the_same_window(dns_records, dns_provider):
    dns_records({('_domainconnect.example.com', 'TXT'): ['api.provider.test'], ('example.com', 'NS'): ['ns1.provider.test.']})
    dns_provider(SETTINGS)
    r = wsgi_post(statelesshosting.app, '/simple_post', HOST, dict(FORM, subdomain='www'))
    assert r['status'] == 200
    assert re.search(r"<a href='https://ux\.provider\.test/v2/domainTemplates/providers/exampleservice\.domainconnect\.org/services/template2/apply"
                     r"\?domain=example\.com&amp;RANDOMTEXT=shm%3A[0-9]+%3AHi&amp;IP=192\.0\.2\.1&amp;host=www"
                     r"&amp;redirect_uri=https%3A%2F%2Fexampleservice\.test%2Fsimple_confirm%3Fdomain%3Dexample\.com%26subdomain%3Dwww&amp;sig=[^']+&amp;key=_dck1'>", r['body'])
    assert 'window.open' not in r['body']


def test_confirm_shows_the_site():
    r = wsgi_get(statelesshosting.app, '/simple_confirm', HOST, query='domain=example.com&subdomain=www')
    assert r['status'] == 200
    assert "href='http://www.example.com'" in r['body']


def test_confirm_shows_the_error():
    r = wsgi_get(statelesshosting.app, '/simple_confirm', HOST, query='domain=example.com&error=access_denied')
    assert 'Synchronous Error' in r['body']
    assert 'access_denied' in r['body']


def test_confirm_serves_only_the_hosting_website():
    assert wsgi_get(statelesshosting.app, '/simple_confirm', 'example.com', query='domain=example.com')['status'] == 404


def test_post_checks_and_signs_template2(dns_records, dns_provider):
    dns_records({('_domainconnect.example.com', 'TXT'): ['api.provider.test'], ('example.com', 'NS'): ['ns1.provider.test.']})
    urls = dns_provider(SETTINGS)
    r = wsgi_post(statelesshosting.app, '/simple_post', HOST, dict(FORM, subdomain='www'))
    assert urls[1:] == ['https://api.provider.test/v2/domainTemplates/providers/exampleservice.domainconnect.org/services/template2']
    href = re.search(r"<a href='(https://ux\.provider\.test/[^']*)'>", r['body']).group(1).replace('&amp;', '&')
    assert href.startswith('https://ux.provider.test/v2/domainTemplates/providers/exampleservice.domainconnect.org/services/template2/apply?')
    qs, sep, signature = href.split('?', 1)[1].partition('&sig=')
    assert 'redirect_uri=https%3A%2F%2Fexampleservice.test%2Fsimple_confirm' in qs
    signature, sep, key = signature.partition('&key=')
    assert key == '_dck1'
    assert sigutil.verify_sig(public_key_pem(), urllib.parse.unquote(signature), qs)
