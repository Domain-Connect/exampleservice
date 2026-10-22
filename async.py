from bottle import Bottle, run, route, template, request, response, abort, static_file, default_app, redirect

import config
import urllib
import util
import json
import requests

@route('/async_index', method='GET')
def async_index():
    return template('async_index.tpl')

@route('/async_post', method='POST')
def async_post():

    # This only works for the hosting website over the supported protocol
    if request.headers['Host'] != config.hosting_website or request.urlparts.scheme != config.protocol:
        return abort(404)

    # Get the domain and hosts
    domain = request.forms.get('domain')
    hosts = request.forms.get('hosts')
    if hosts is None:
        hosts = ''
    if domain == None or domain == '' or not util.is_valid_hostname(domain):
        return template('invalid_data.tpl')

    # See if the DNS Provider supports domain connect
    json_data, txt, error_message = util.get_domainconnect_json(domain)
    if json_data == None:
        return template('no_domain_connect.tpl', {'reason' : str(error_message)})

    # Get the provider name
    dns_provider = json_data['providerName']

    # See if our templates are supported
    check_url1 = json_data['urlAPI'] + '/v2/domainTemplates/providers/' + config.provider + '/services/' + config.template1
    check_url2 = json_data['urlAPI'] + '/v2/domainTemplates/providers/' + config.provider + '/services/' + config.template2
    if not util.check_template(check_url1) or not util.check_template(check_url2):
        return template('no_domain_connect.tpl', {'reason' : 'Missing template support'})

    # Verify that the provider supports async
    if not dns_provider in config.oAuthSecrets or not dns_provider in config.oAuthAPIURLs or config.oAuthAPIURLs[dns_provider] != json_data['urlAPI']:
        return template('no_domain_connect.tpl', {'reason' : 'Not onboarded as oAuth provider'})

    # The redirect_url is part of oAuth and where the user will be sent after consent. Appended to this URL will be the OAuth code or an error
    redirect_url = config.protocol + "://" + config.hosting_website + "/async_oauth_response?domain=" + domain + "&hosts=" + hosts + "&dns_provider=" + dns_provider

    # Right now the call to get a permission requires the template in the path. Doesn't matter which one.  Spec is updating to eliminate this

    asynchronousUrl = json_data['urlAsyncUX'] + '/v2/domainTemplates/providers/' + config.provider + '?' + \
            "domain=" + domain + \
            "&host=" + hosts + \
            "&client_id=" + config.provider + \
            "&scope=" + config.template1 + '+' + config.template2 + \
            "&redirect_uri=" + urllib.parse.quote(redirect_url, '')

    return template('async_post.tpl',
		{
                    'txt': txt,
                    'json': json.dumps(json_data),
                    'check_url1' : check_url1,
                    'check_url2' : check_url2,
                    'domain': domain,
                    'hosts': hosts,
                    'providerName' : json_data['providerName'], 
                    'asynchronousUrl': asynchronousUrl
                })                    
                    
# Handle the redirect back from the oAuth call
#
# Normally this would get the access token, store it, and then redirect to some other page on the client.
#
# Here we get the access token and simply return it to the client. The client will post it back to emulate 
# the async server call
@route("/async_oauth_response")
def async_oauth_response():

    # This only works for the hosting website over the supported protocol
    if request.headers['Host'] != config.hosting_website or request.urlparts.scheme != config.protocol:
        return abort(404)

    # Get the data from the URL
    code = request.query.get("code")
    domain = request.query.get("domain")
    hosts = request.query.get("hosts")
    dns_provider = request.query.get('dns_provider')
    error = request.query.get('error')
    
    if error != None and error != '':
        return template('async_error',
                    {
                        'error': 'Error returned from DNSProvider (' + error + ')'
                    })

    # The original redirect url when getting the access token
    redirect_url = config.protocol + "://" + config.hosting_website + "/async_oauth_response?domain=" + domain + "&hosts=" + hosts + "&dns_provider=" + dns_provider

    # Take the oauth code and get an access token. This must be done fairly quickly as oauth codes have a short expiry
    url = config.oAuthAPIURLs[dns_provider] + "/v2/oauth/access_token?code=" + code + "&grant_type=authorization_code&client_id=" + config.provider + "&client_secret=" + urllib.parse.quote(config.oAuthSecrets[dns_provider], '') + "&redirect_uri=" + urllib.parse.quote(redirect_url, '')
        
    # Call the oauth provider and get the access token
    r = requests.post(url, verify=True)
    if r.status_code >= 300:
        return template('async_error',
                        {
                        'error': 'Error getting access_token: ' +  r.text
                        })

    json_response = r.json()
    access_token = json_response['access_token']

    # Return a page. Normally you would store the access and re-auth tokens and redirect the client browser
    return template('async_oauth_response.tpl',
        {
            "code": code, 

            "url": url,

            "domain": domain, 
            "hosts" : hosts, 
            "dns_provider": dns_provider,

            "access_token" : access_token, 
            "json_response": json.dumps(json_response), 

        })

# Handle the form post for the processing the asynchronous setting using an oAuth access token. 
@route("/async_confirm", method='POST')
def async_confirm():

    # This only works for the hosting website over the supported protocol
    if request.headers['Host'] != config.hosting_website or request.urlparts.scheme != config.protocol:
        return abort(404)

    # Get the domain name, message, acccess token
    domain = request.forms.get('domain')
    subdomain = request.forms.get('subdomain')
    hosts = request.forms.get('hosts')
    message = request.forms.get('message')
    access_token = request.forms.get('access_token')
    dns_provider = request.forms.get('dns_provider')
    force = request.forms.get('force')
    if force == None or force == '':
        force = 0
    else:
        force = 1

    # Validate the form settings
    if domain == None or domain == '' or not util.is_valid_hostname(domain) or message == None or message == '' or not util.is_valid_message(message) or access_token == None or access_token == '' or dns_provider == None or dns_provider == '':
        return template('invalid_data.tpl')

    dns_message_data = util.dns_message_data(message)

    # This is the URL to call the api to apply the template
    if 'template2' in request.forms.keys():
        url = config.oAuthAPIURLs[dns_provider] + '/v2/domainTemplates/providers/' + config.provider + '/services/' + config.template2 + '/apply?domain=' + domain + '&host=' + subdomain + '&force=' + str(force) + '&RANDOMTEXT=' + dns_message_data + '&IP=' + config.ip
        applied_template = 'Template 2'
    else:
        url = config.oAuthAPIURLs[dns_provider] + '/v2/domainTemplates/providers/' + config.provider + '/services/' + config.template1 + '/apply?domain=' + domain + '&host=' + subdomain + '&force=' + str(force) + '&RANDOMTEXT=' + dns_message_data + '&IP=' + config.ip
        applied_template = 'Template 1'

    # Call the api with the oauth acces bearer token

    r = requests.post(url, headers={'Authorization': 'Bearer ' + access_token}, verify=True)

    # If this fails, and there is a re-auth token, we could add this code here

    # Return a page. Normally you would store the access and re-auth tokens and redirect the client browser
    return template('async_confirm.tpl', 
        {"applied_template": applied_template,
         "url": url,
         "message" : message,
         "access_token" : access_token, 
         "domain": domain, 
         "subdomain": subdomain,
         "hosts": hosts,
         "dns_provider" : dns_provider,
         "status_code" : str(r.status_code)
     })

