#-----------------------------------------------------------------
# Signature tools
#

from bottle import Bottle, run, route, template, request, response, abort, static_file, default_app, redirect

import urllib
import urlparse

import util
import config

@route('/sig', method='GET')
def sig():    

    # This only works for the hosting website over the supported protocol
    if request.headers['Host'] != config.hosting_website or request.urlparts.scheme != config.protocol:
        return abort(404)

    return template('sig.tpl')

@route('/sig_generate', method='POST')
def sig_generate():

    # This only works for the hosting website over the supported protocol
    if request.headers['Host'] != config.hosting_website or request.urlparts.scheme != config.protocol:
        return abort(404)

    qs = request.forms.get('qs')
    priv = request.forms.get('privatekey')
    if priv:
        priv = priv.replace('\\n', '')
        priv = priv.replace('\n', '')
        priv = priv.replace(' ', '')
        priv = '-----BEGIN PRIVATE KEY-----\n' + priv + '\n-----END PRIVATE KEY-----\n'
    else:
        priv = config.priv_key

    sig = util.generate_sig(priv, qs)

    return template('sig_generate.tpl',
                    {
                        'sig': sig
                    }
                    )

@route('/sig_fetch', method='POST')
def sig_fetch():
    # This only works for the hosting website over the supported protocol
    if request.headers['Host'] != config.hosting_website or request.urlparts.scheme != config.protocol:
        return abort(404)

    domain = request.forms.get('domain')
    key = request.forms.get('key')

    try:
        pub_key, record_strings = util.get_publickey(key + "." + domain)
        pub_key = '-----BEGIN PUBLIC KEY-----\n' + pub_key + '\n-----END PUBLIC KEY-----\n'
    except:
        pub_key = None
        record_strings = []

    return template('sig_fetch.tpl',
		{
                    'domain' : domain,
                    'key': key,
                    'pubKey': pub_key,
                    'record_strings': record_strings
                })                    


@route('/sig_verify', method='POST')
def sig_verify():

    # This only works for the hosting website over the supported protocol
    if request.headers['Host'] != config.hosting_website or request.urlparts.scheme != config.protocol:
        return abort(404)

    # Get the domain/message and validate
    domain = request.forms.get('domain')
    key = request.forms.get('key')
    pub = request.forms.get('publickey')
    if pub:
        pub = pub.replace('\\n', '')
        pub = pub.replace(' ', '')
        pub = '-----BEGIN PUBLIC KEY-----\n' + pub + '\n-----END PUBLIC KEY-----\n'
    sig = request.forms.get('sig')
    qs = request.forms.get('qs')

    if not pub:
        try:
            pub, record_strings = util.get_publickey(key + "." + domain)
            pub = '-----BEGIN PUBLIC KEY-----\n' + pub + '\n-----END PUBLIC KEY-----\n'
        except:
            pub = None
            record_strings = []
    else:
        record_strings = []

    try:
        verified = util.verify_sig(pub, sig, qs)
    except:
        verified = False

    return template('sig_verify.tpl',
		{
                    'domain' : domain,
                    'key': key,
                    'sig': sig,
                    'qs': qs,
                    'verified': verified,
                    'pubKey': pub,
                    'record_strings': record_strings
                })                    

@route('/sig_verify_url', method='POST')
def sig_verify_url():

    # This only works for the hosting website over the supported protocol
    if request.headers['Host'] != config.hosting_website or request.urlparts.scheme != config.protocol:
        return abort(404)

    # Get the domain/message and validate
    url = request.forms.get('url')
    domain = request.forms.get('domain')

    params = urlparse.urlparse(url).query.split('&')
    sig = None
    key = None
    qs = None
    for param in params:
        if param.startswith('sig='):
            sig = urllib.unquote(param[4:])
        elif param.startswith('key='):
            key = urllib.unquote(param[4:])
        else:
            if not qs:
                qs = param
            else:
                qs = qs + '&' + param

    try:
        pub, record_strings = util.get_publickey(key + "." + domain)
        pub = '-----BEGIN PUBLIC KEY-----\n' + pub + '\n-----END PUBLIC KEY-----\n'
    except:
        pub = None
        record_strings = []

    try:
        verified = util.verify_sig(pub, sig, qs)
    except:
        verified = False

    return template('sig_verify.tpl',
		{
                    'domain' : domain,
                    'key': key,
                    'sig': sig,
                    'qs': qs,
                    'verified': verified,
                    'pubKey': pub,
                    'record_strings': record_strings
                })                    


