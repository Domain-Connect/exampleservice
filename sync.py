from bottle import Bottle, run, route, template, request, response, abort, static_file, default_app, redirect

import urllib

import config
import util
import json

@route('/sync_index', method='GET')
def sync_index():
    return template('sync_index.tpl')
        

@route('/sync_post', method='POST')
def sync_post():
    
    # This only works for the hosting website over the supported protocol
    if request.headers['Host'] != config.hosting_website or request.urlparts.scheme != config.protocol:
        return abort(404)


    # Get the domain/message and validate
    domain = request.forms.get('domain')
    subdomain = request.forms.get('subdomain')
    message = request.forms.get('message')
    if domain == None or domain == '' or not util.is_valid_hostname(domain) or message == None or message == '' or not util.is_valid_message(message):
        return template('invalid_data.tpl')

    # See if the DNS Provider supports domain connect
    json_data, txt = util.get_domainconnect_json(domain)
    if json_data == None:
        return template('no_domain_connect.tpl', {'reason' : 'Unable to read configuration'})

    width = 750
    if json_data.has_key('width'):
        width = json_data['width']

    height = 750
    if json_data.has_key('height'):
        height =json_data['height']
    

    # See if our templates are supported
    check_url1 = json_data['urlAPI'] + '/v2/domainTemplates/providers/' + config.provider + '/services/' + config.template1
    check_url2 = json_data['urlAPI'] + '/v2/domainTemplates/providers/' + config.provider + '/services/' + config.template2
    if not util.check_template(check_url1) or not util.check_template(check_url2):
        return template('no_domain_connect.tpl', {'reason' : 'Missing template support'})

    dns_message_data = util.dns_message_data(message)
		
    # Generate the query string for synchronous calls
    qs = 'domain=' + urllib.quote(domain, '') + '&RANDOMTEXT=' + urllib.quote(dns_message_data) + '&IP=' + urllib.quote(config.ip, '')
    if subdomain != '' and subdomain != None:
        qs = qs + '&host=' + urllib.quote(subdomain, '')

    # Create the URL to configure template 1
    synchronousUrl1 = json_data['urlSyncUX'] + '/v2/domainTemplates/providers/' + config.provider + '/services/' + config.template1 + '/apply?' + qs
	
    # Create the URL to configure template2. Template 2 needs a singature
    sig = util.generate_sig(config.priv_key, qs)
    synchronousSignedUrl2 = json_data['urlSyncUX'] + '/v2/domainTemplates/providers/' + config.provider + '/services/' + config.template2 + '/apply?' + qs + '&sig=' + urllib.quote(sig, '') + '&key=_dck1'

    # Generate the redirect uri
    redirect_uri = config.protocol + "://" + config.hosting_website + "/sync_confirm?domain=" + domain + "&subdomain=" + subdomain

    # Query string with the redirect
    qsRedirect = qs + "&redirect_uri=" + urllib.quote(redirect_uri, '')

    # Create the URL to configure template 1 with a redirect back
    synchronousRedirectUrl1 = json_data['urlSyncUX'] + '/v2/domainTemplates/providers/' + config.provider + '/services/' + config.template1 + '/apply?' + qsRedirect

    # Create the URL to configure template 2 with a redirect back. Template 2 needs a signature
    sigRedirect = util.generate_sig(config.priv_key, qsRedirect)
    synchronousSignedRedirectUrl2 = json_data['urlSyncUX'] + '/v2/domainTemplates/providers/' + config.provider + '/services/' + config.template2 + '/apply?' + qsRedirect + '&sig=' + urllib.quote(sigRedirect, '') + '&key=_dck1'
    
    return template('sync_post.tpl',
		{
                    'txt': txt,
                    'json': json.dumps(json_data),
                    'check_url1' : check_url1,
                    'check_url2' : check_url2,
                    'domain': domain,
                    'providerName' : json_data['providerName'], 
                    'width': width,
                    'height': height,
                    'synchronousUrl1' : synchronousUrl1, 
                    'synchronousSignedUrl2' : synchronousSignedUrl2,
                    'qs': qs,
                    'sig': sig,
                    'synchronousRedirectUrl1' : synchronousRedirectUrl1, 
                    'synchronousSignedRedirectUrl2' : synchronousSignedRedirectUrl2,
                    'qsRedirect' : qsRedirect,
                    'sigRedirect': sigRedirect
                })                    

@route('/sync_confirm', method='GET')
def sync_confirm():

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

    return template('sync_confirm.tpl',
                    {
                        'domain': domain,
                        'subdomain': subdomain
                    })

