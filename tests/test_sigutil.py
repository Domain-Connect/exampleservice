from cryptography.hazmat.primitives import serialization

import config
import sigutil

QUERY = 'domain=example.com&RANDOMTEXT=shm%3A1%3AHi&IP=192.0.2.1'


def public_key_pem():
    private_key = serialization.load_pem_private_key(config.priv_key.encode('ascii'), password=None)
    return private_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('ascii')


def public_key_body():
    return ''.join(public_key_pem().splitlines()[1:-1])


def test_sign_and_verify():
    sig = sigutil.generate_sig(config.priv_key, QUERY)
    assert sigutil.verify_sig(public_key_pem(), sig, QUERY)


def test_changed_query_fails_verification():
    sig = sigutil.generate_sig(config.priv_key, QUERY)
    assert not sigutil.verify_sig(public_key_pem(), sig, QUERY + '&host=www')


def test_public_key_joined_in_p_order(dns_records):
    body = public_key_body()
    dns_records({('_dck1.example.com', 'TXT'): [
        'p=2,a=RS256,t=x509,d=' + body[200:],
        'p=1,a=RS256,t=x509,d=' + body[:200],
    ]})
    key, records = sigutil.get_publickey('_dck1.example.com')
    assert key == body
    assert len(records) == 2


def test_public_key_with_other_algorithm_is_rejected(dns_records):
    dns_records({('_dck1.example.com', 'TXT'): ['p=1,a=RS1,t=x509,d=' + public_key_body()]})
    assert sigutil.get_publickey('_dck1.example.com') == (None, None)
