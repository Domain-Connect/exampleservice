import statelesshosting
from conftest import wsgi_get

HOST = 'exampleservice.test'


def test_home_page_links_every_flow():
    r = wsgi_get(statelesshosting.app, '/', HOST)
    assert r['status'] == 200
    for link in ['/simple_index', '/sync_index', '/async_index', '/sig',
                 'exampleservice.domainconnect.org.template1.json',
                 'exampleservice.domainconnect.org.template2.json']:
        assert link in r['body']


def test_home_page_over_http_redirects_to_https():
    r = wsgi_get(statelesshosting.app, '/', HOST, scheme='http')
    assert r['status'] == 302
    assert r['headers']['Location'] == 'https://' + HOST


def test_hosted_site_renders_messages_in_time_order(dns_records):
    dns_records({('example.com', 'TXT'): ['shm:200:second', 'v=spf1 -all', 'shm:100:first']})
    r = wsgi_get(statelesshosting.app, '/', 'example.com', scheme='http')
    assert r['status'] == 200
    assert 'first<br>second<br>' in r['body']


def test_hosted_site_without_message_is_404(dns_records):
    dns_records({})
    r = wsgi_get(statelesshosting.app, '/', 'example.com', scheme='http')
    assert r['status'] == 404


def test_flow_pages_render():
    for path in ['/simple_index', '/sync_index', '/async_index', '/sig', '/client']:
        assert wsgi_get(statelesshosting.app, path, HOST)['status'] == 200


def test_flow_pages_serve_only_the_hosting_website():
    for path in ['/simple_index', '/sig', '/client']:
        assert wsgi_get(statelesshosting.app, path, 'example.com')['status'] == 404
