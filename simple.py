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

@route('/simple_index', method='GET')
def simple_index():

    # This only works for the ddns wesbsite over the supported protocol
    if request.headers['Host'] != config.hosting_website or request.urlparts.scheme != config.protocol:
        return abort(404)

    return template('simple_index.tpl')

@route('/simple_post', method='POST')
def simple_post():
    # Get the domain/message and validate
    domain = request.forms.get('domain')
    subdomain = request.forms.get('subdomain')
    message = request.forms.get('message')
    if domain == None or domain == '' or not util.is_valid_hostname(domain) or message == None or message == '' or not util.is_valid_message(message):
        return template('invalid_data.tpl')

    # See if the DNS Provider supports domain connect
    json_data, txt, error_message = util.get_domainconnect_json(domain)
    if json_data == None:
        return template('no_domain_connect.tpl', {'reason' : str(error_message)})

    width = 750
    if 'width' in json_data:
        width = json_data['width']

    height = 750
    if 'height' in json_data:
        height =json_data['height']
    
    # See if our template is supported
    check_url1 = json_data['urlAPI'] + '/v2/domainTemplates/providers/' + config.provider + '/services/' + config.template1
    if not util.check_template(check_url1):
        return template('no_domain_connect.tpl', {'reason' : 'Missing template support'})

    dns_message_data = util.dns_message_data(message)
		
    # Generate the query string for synchronous calls
    qs = 'domain=' + urllib.parse.quote(domain, '') + '&RANDOMTEXT=' + urllib.parse.quote(dns_message_data) + '&IP=' + urllib.parse.quote(config.ip, '')
    if subdomain != '' and subdomain != None:
        qs = qs + '&host=' + urllib.parse.quote(subdomain, '')

    # Create the URL to configure template 1
    synchronousUrl1 = json_data['urlSyncUX'] + '/v2/domainTemplates/providers/' + config.provider + '/services/' + config.template1 + '/apply?' + qs

    fqdn = domain
    if subdomain:
        fqdn = subdomain + '.' + fqdn
	
    return template('simple_post.tpl',
		{
                    'providerName' : json_data['providerName'], 
                    'width': width,
                    'height': height,
                    'synchronousUrl1' : synchronousUrl1,
                    'fqdn': fqdn
                })                    

