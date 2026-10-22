#----------------------------------------------------------------------------------
# Simple Flow
#
# This is a simple flow for setting up stateless hosting using Domain Connect. It
# shows what the user would typically see
#

from bottle import Bottle, run, route, template, request, response, abort, static_file, default_app, redirect

import urllib.parse

import config
import util
import sigutil

@route('/simple_index', method='GET')
def simple_index():

    # This only works for the ddns wesbsite over the supported protocol
    if request.headers['Host'] != config.hosting_website or request.urlparts.scheme != config.protocol:
        return abort(404)

    return template('simple_index.tpl', {'dc_txt': request.query.get('dc_txt') or '', 'dc_proto': request.query.get('dc_proto') or ''})

@route('/simple_post', method='POST')
def simple_post():
    # Get the domain/message and validate
    domain = request.forms.get('domain')
    subdomain = request.forms.get('subdomain')
    message = request.forms.get('message')
    dc_txt = request.forms.get('dc_txt')
    dc_proto = request.forms.get('dc_proto')
    if domain == None or domain == '' or not util.is_valid_hostname(domain) or message == None or message == '' or not util.is_valid_message(message) or (dc_txt and not util.is_valid_dc_txt(dc_txt)) or (dc_proto and not util.is_valid_dc_proto(dc_proto)):
        return template('invalid_data.tpl')

    # See if the DNS Provider supports domain connect
    json_data, txt, error_message = util.get_domainconnect_json(domain, dc_txt, dc_proto)
    if json_data == None:
        return template('no_domain_connect.tpl', {'reason' : str(error_message)})

    # See if our template is supported
    check_url2 = json_data['urlAPI'] + '/v2/domainTemplates/providers/' + config.provider + '/services/' + config.template2
    if not util.check_template(check_url2):
        return template('no_domain_connect.tpl', {'reason' : 'Missing template support'})

    dns_message_data = util.dns_message_data(message)
		
    # Generate the query string for synchronous calls
    qs = 'domain=' + urllib.parse.quote(domain, '') + '&RANDOMTEXT=' + urllib.parse.quote(dns_message_data) + '&IP=' + urllib.parse.quote(config.ip, '')
    if subdomain != '' and subdomain != None:
        qs = qs + '&host=' + urllib.parse.quote(subdomain, '')

    # The DNS Provider sends the user back to redirect_uri after applying the template
    redirect_uri = config.protocol + '://' + config.hosting_website + '/simple_confirm?domain=' + urllib.parse.quote(domain, '') + '&subdomain=' + urllib.parse.quote(subdomain or '', '')
    qs = qs + '&redirect_uri=' + urllib.parse.quote(redirect_uri, '')

    # Create the URL to configure template 2. Template 2 needs a signature
    sig = sigutil.generate_sig(config.priv_key, qs)
    synchronousSignedRedirectUrl2 = json_data['urlSyncUX'] + '/v2/domainTemplates/providers/' + config.provider + '/services/' + config.template2 + '/apply?' + qs + '&sig=' + urllib.parse.quote(sig, '') + '&key=_dck1'
	
    return template('simple_post.tpl',
		{
                    'providerName' : json_data['providerName'], 
                    'dc_txt': dc_txt,
                    'synchronousSignedRedirectUrl2' : synchronousSignedRedirectUrl2
                })                    

@route('/simple_confirm', method='GET')
def simple_confirm():

    # This only works for the hosting website over the supported protocol
    if request.headers['Host'] != config.hosting_website or request.urlparts.scheme != config.protocol:
        return abort(404)

    domain = request.query.get('domain')
    subdomain = request.query.get('subdomain')
    error = request.query.get('error')

    if error != None and error != '':
        return template('sync_error.tpl',
                        {
                            'error': error
                        })

    fqdn = domain
    if subdomain:
        fqdn = subdomain + '.' + fqdn

    return template('simple_confirm.tpl',
                    {
                        'fqdn': fqdn
                    })

