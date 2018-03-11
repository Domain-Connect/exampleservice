from bottle import Bottle, run, route, template, request, response, abort, static_file, default_app
from dns.resolver import dns

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode, b64encode,urlsafe_b64decode,b16encode

import requests
import json
import urllib
import re
import time
import calendar

# This is the IP address of the server running this code. You can run the
# sample on localhost, but you'll need to edit your host file
_ip = '132.148.25.185'

# This is the host name of our application
_hosting_website = 'exampleservice.domainconnect.org'

# This is the private key used to generate signatures.
#
#  Normally a private key isn't put into code.  But this is a simple sample application.
priv_key = '-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA18SgvpmeasN4BHkkv0SBjAzIc4grYLjiAXRtNiBUiGUDMeTzQrKTsWvy9NuxU1dIHCZy9o1CrKNg5EzLIZLNyMfI6qiXnM+HMd4byp97zs/3D39Q8iR5poubQcRaGozWx8yQpG0OcVdmEVcTfyR/XSEWC5u16EBNvRnNAOAvZYUdWqVyQvXsjnxQot8KcK0QP8iHpoL/1dbdRy2opRPQ2FdZpovUgknybq/6FkeDtW7uCQ6Mvu4QxcUa3+WP9nYHKtgWip/eFxpeb+qLvcLHf1h0JXtxLVdyy6OLk3f2JRYUX2ZZVDvG3biTpeJz6iRzjGg6MfGxXZHjI8weDjXrJwIDAQABAoIBAGiPedJDwXg9d1i7mCo0OY8z1qPeFh9OGP/Zet8i9bQPN2gjahslTNtK07cDC8C2aFRz8Xw3Ylsk5VxdNobzjFPDNUM6JhawnvR0jQU5GhdTwoc5DHH7aRRjTP6m938sRx0VrfZwfvJAB09Z4jHX7vyjfvprH9EH8GQ2L5lACtfnsSASVJB77H1vtgxTnum74CSqIck1MCjPD/TVUtYfMJwkUQWcbk79N4nvnEoagqsDrvw4okU2OYMWucQjyxfWTU4NGlsDScRbdDAb8sLr3DpMfXM8vpZJ3Ed6gfw14hEJym8XoHwDHmjGmgYH9iG6MODxuO5TLRmRR6b+jcUV/2kCgYEA4WGsDUO/NIXIqtDm5lTi5qeFl0sGKIgRLGuCrvjLF0Fq5Yx28wuow3OhZ3rbjlmhf9nUt24nUUY67plv2pi+vx3kVdbcNfk+Wkc0wfx8+U91qaTplMRhNjrnq/Kp9E7xtnzZRInpUG1Ha5ozTYobVvklUvjodFlF2c16Zz2X2AMCgYEA9RSeZm7oMyJbe985SScXruwt5ZXlUBoBLDZAeMloPpaqknFmSVSNgtniywztF8HppJQyiMvmUOUL2tKnuShXwsvTkCTBC/vNGXutiPS8O2yqeQ8dHoHuKcoMFwgajrbPrVkuFtUkjbQJ/TKoZtrxUdCryDZ/AHmRtiHh9E4NUQ0CgYAE7ngvSh4y7gJ4Cl4jCBR26492wgN+e4u0px2S6oq3FY1bPHmV09l7fVo4w21ubfOksoV/BgACPUEo216hL9psoCDQ6ASlgbCllQ1IeVfatKxka+FYift+jkdnccXaPKf5UD4Iy+O5CMsZRaR9u9nhS05PxHaBpTpsC5z0CVr7NQKBgQCsBTzpSQ9SVNtBpvzei8Hj1YKhkwTRpG8OSUYXgcbZp4cyIsZY0jBBmA3H19rSwhjsm9icjAGs5hfcD+AJ5nczEz37/tBBSQw8xsKXTrCQRUWikyktMKWqT1cNE3MQmOBMHDxtak2t6KDaR6RMDYE0m/L3JMkf3DSaUk323JIcQQKBgD6lHhw79Cenpezzf0566uWE1QF6Sv3kWk6Gkzo2jUGmjo2tG1v2Nj82DvcTuqvfUKSr2wTKINxnKGyYXGto0BykdxeFbR04cNcBB46zUjasro2ZCvIoAHCpohNBI2dL6dI+RI3jC/KY3jPNI0toaOTWkeAvJ7w09G2ttlv8qLNV\n-----END RSA PRIVATE KEY-----'

# The corresponding public key is:
#
#pub_key = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA18SgvpmeasN4BHkkv0SBjAzIc4grYLjiAXRtNiBUiGUDMeTzQrKTsWvy9NuxU1dIHCZy9o1CrKNg5EzLIZLNyMfI6qiXnM+HMd4byp97zs/3D39Q8iR5poubQcRaGozWx8yQpG0OcVdmEVcTfyR/XSEWC5u16EBNvRnNAOAvZYUdWqVyQvXsjnxQot8KcK0QP8iHpoL/1dbdRy2opRPQ2FdZpovUgknybq/6FkeDtW7uCQ6Mvu4QxcUa3+WP9nYHKtgWip/eFxpeb+qLvcLHf1h0JXtxLVdyy6OLk3f2JRYUX2ZZVDvG3biTpeJz6iRzjGg6MfGxXZHjI8weDjXrJwIDAQAB\n-----END PUBLIC KEY-----'
##
# This is in DNS for _dck1.exampleservice.domainconnect.org contains TXT records of the form:
#
#    p=1,a=RS256,t=x509,d=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA18SgvpmeasN4BHkkv0SBjAzIc4grYLjiAXRtNiBUiGUDMeTzQrKTsWvy9NuxU1dIHCZy9o1CrKNg5EzLIZLNyMfI6qiXnM+HMd4byp97zs/3D39Q8iR5poubQcRaGozWx8yQpG0OcVdmEVcTfy
#    p=2,a=RS256,t=x509,d=R/XSEWC5u16EBNvRnNAOAvZYUdWqVyQvXsjnxQot8KcK0QP8iHpoL/1dbdRy2opRPQ2FdZpovUgknybq/6FkeDtW7uCQ6Mvu4QxcUa3+WP9nYHKtgWip/eFxpeb+qLvcLHf1h0JXtxLVdyy6OLk3f2JRYUX2ZZVDvG3biTpeJz6iRzjGg6MfGxXZHjI8
#    p=3,a=RS256,t=x509,d=weDjXrJwIDAQAB
#

# Domain Connect Provider and Service/Template
#
# These templates takes two variables. The IP address for the A Record (IP=), and string put into a TXT record (RANDOMTEXT=). These are usedn
# to set an A record and a TXT record into the zone. 
#
# The 2nd variant adds a CNAME with the host value of WHD (a holdover from a hackathon where this was initially created)

_provider = 'exampleservice.domainconnect.org'
_template1 = 'template1'
_template2 = 'template2'

# Secrets per provider that support oAuth
oAuthSecrets = {
    'GoDaddy' : 'DomainConnectGeheimnisSecretString',
    'Secure Server' : 'DomainConnectGeheimnisSecretString',
    '1and1': 'cd$;CVZRj#B8C@o3o8E4v-*k2H7S%)'
}

oAuthAPIURLs = {
    'GoDaddy' : 'https://domainconnect.api.godaddy.com',
    'Secure Server' : 'https://domainconnect.api.secureserver.net',
    '1and1' : 'https://api.domainconnect.1and1.com'
}

app = default_app()

# Handle the home page. This can be rendered for the service, or the individual sites
@route('/')
def index():

    # If the host is my hosting website, render the home page
    if request.headers['Host'] == _hosting_website:
        return template('index.tpl', {})
    else:
        # See if the text string was put into DNS
        messagetext = _get_messagetext(request.headers['Host'])

        # We only render a site for domains that have been configured with a message
        if messagetext == None or messagetext == '':
            return abort(404)

        # Render the site 
        return template('site.tpl', {'host': request.headers['Host'], 'messagetext': messagetext})

@route('/sync', method='POST')
def sync():
    
    # This only works for the hosting website
    if request.headers['Host'] != _hosting_website:
        return abort(404)

    # Get the domain/message and validate
    domain = request.forms.get('domain')
    subdomain = request.forms.get('subdomain')
    message = request.forms.get('message')
    if domain == None or domain == '' or not _is_valid_hostname(domain) or message == None or message == '' or not _is_valid_message(message):
        return template('invalid_data.tpl')

    # See if the DNS Provider supports domain connect
    json_data, txt = _get_domainconnect_json(domain)
    if json_data == None:
        return template('no_domain_connect.tpl', {'reason' : 'Unable to read configuration'})

    width = 750
    if json_data.has_key('width'):
        width = json_data['width']

    height = 750
    if json_data.has_key('height'):
        height =json_data['height']
    

    # See if our templates are supported
    check_url1 = json_data['urlAPI'] + '/v2/domainTemplates/providers/' + _provider + '/services/' + _template1
    check_url2 = json_data['urlAPI'] + '/v2/domainTemplates/providers/' + _provider + '/services/' + _template2
    if not _check_template(check_url1) or not _check_template(check_url2):
        return template('no_domain_connect.tpl', {'reason' : 'Missing template support'})

    secs = calendar.timegm(time.gmtime()) # Seconds since the epoch
		
    # Generate the query string for synchronous calls
    qs = 'domain=' + urllib.quote(domain) + '&RANDOMTEXT=' + urllib.quote('shm:' + str(secs) + ':' + message) + '&IP=' + urllib.quote(_ip)
    if subdomain != '' and subdomain != None:
        qs = qs + '&host=' + urllib.quote(subdomain)

    # Create the URL to configure template 1
    synchronousUrl1 = json_data['urlSyncUX'] + '/v2/domainTemplates/providers/' + _provider + '/services/' + _template1 + '/apply?' + qs
	
    # Create the URL to configure template2. Template 2 needs a singature
    sig = _generate_sig(priv_key, qs)
    synchronousSignedUrl2 = json_data['urlSyncUX'] + '/v2/domainTemplates/providers/' + _provider + '/services/' + _template2 + '/apply?' + qs + '&sig=' + urllib.quote(sig) + '&key=_dck1'

    # Generate the redirect uri
    redirect_uri = "http://" + _hosting_website + "/sync_confirm?domain=" + domain + "&subdomain=" + subdomain

    # Query string with the redirect
    qsRedirect = qs + "&redirect_uri=" + urllib.quote(redirect_uri)

    # Create the URL to configure template 1 with a redirect back
    synchronousRedirectUrl1 = json_data['urlSyncUX'] + '/v2/domainTemplates/providers/' + _provider + '/services/' + _template1 + '/apply?' + qsRedirect

    # Create the URL to configure template 2 with a redirect back. Template 2 needs a signature
    sigRedirect = _generate_sig(priv_key, qsRedirect)
    synchronousSignedRedirectUrl2 = json_data['urlSyncUX'] + '/v2/domainTemplates/providers/' + _provider + '/services/' + _template2 + '/apply?' + qsRedirect + '&sig=' + urllib.quote(sigRedirect) + '&key=_dck1'
    
    # For fun, verify the signatures.  Mostly to show how a DNS Provider would do this.
    pub_key = _get_publickey('_dck1.' + _hosting_website)
    verified = _verify_sig(pub_key, sig, qs)
    verifiedRedirect = _verify_sig(pub_key, sigRedirect, qsRedirect)

    return template('sync.tpl',
		{
                    'txt': txt,
                    'json': json.dumps(json_data),
                    'domain': domain,
                    'providerName' : json_data['providerName'], 
                    'width': width,
                    'height': height,
                    'synchronousUrl1' : synchronousUrl1, 
                    'synchronousSignedUrl2' : synchronousSignedUrl2,
                    'qs': qs,
                    'sig': sig,
                    'verified': verified,
                    'synchronousRedirectUrl1' : synchronousRedirectUrl1, 
                    'synchronousSignedRedirectUrl2' : synchronousSignedRedirectUrl2,
                    'qsRedirect' : qsRedirect,
                    'sigRedirect': sigRedirect,
                    'verifiedRedirect': verifiedRedirect,
                    'pubKey': pub_key
                })                    

@route('/sync_confirm', method='GET')
def sync_confirm():
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

@route('/async', method='POST')
def async():

    # This only works for the hosting website
    if request.headers['Host'] != _hosting_website:
        return abort(404)

    # Get the domain and hosts
    domain = request.forms.get('domain')
    hosts = request.forms.get('hosts')
    if hosts is None:
        hosts = ''
    if domain == None or domain == '' or not _is_valid_hostname(domain):
        return template('invalid_data.tpl')

    # See if the DNS Provider supports domain connect
    json_data, txt = _get_domainconnect_json(domain)
    if json_data == None:
        return template('no_domain_connect.tpl', {'reason' : 'Unable to read configuration'})

    # Get the provider name
    dns_provider = json_data['providerName']

    # See if our templates are supported
    check_url1 = json_data['urlAPI'] + '/v2/domainTemplates/providers/' + _provider + '/services/' + _template1
    check_url2 = json_data['urlAPI'] + '/v2/domainTemplates/providers/' + _provider + '/services/' + _template2
    if not _check_template(check_url1) or not _check_template(check_url2):
        return template('no_domain_connect.tpl', {'reason' : 'Missing template support'})

    # Verify that the provider supports async
    if not oAuthSecrets.has_key(dns_provider) or not oAuthAPIURLs.has_key(dns_provider) or oAuthAPIURLs[dns_provider] != json_data['urlAPI']:
        return template('no_domain_connect.tpl', {'reason' : 'Not onboarded as oAuth provider'})

    # The redirect_url is part of oAuth and where the user will be sent after consent. Appended to this URL will be the OAuth code or an error
    redirect_url = "http://" + _hosting_website + "/async_oauth_response?domain=" + domain + "&hosts=" + hosts + "&dns_provider=" + dns_provider

    # Right now the call to get a permission requires the template in the path. Doesn't matter which one.  Spec is updating to eliminate this
    asynchronousUrl = json_data['urlAsyncUX'] + '/v2/domainTemplates/providers/' + _provider + '/services/' + _template1 + '?' + \
            'domain=' + domain + \
            "&client_id=" + _provider + \
            "&scope=" + _template1 + ' ' + _template2 + \
            "&redirect_uri=" + urllib.quote(redirect_url)

    asynchronousUrl3 = json_data['urlAsyncUX'] + '/v2/domainTemplates/providers/' + _provider + '/services/' + _template1 + '?' + \
            'domain=' + domain + \
            "&client_id=" + _provider + \
            "&scope=" + _template1 + ' ' + _template2 + \
            "&redirect_uri=" + urllib.quote(redirect_url + 'code_only=1')

    asynchronousUrl2 = json_data['urlAsyncUX'] + '/v2/domainTemplates/providers/' + _provider + '?' + \
            'domain=' + domain + \
            "&client_id=" + _provider + \
            "&scope=" + _template1 + ' ' + _template2 + \
            "&redirect_uri=" + urllib.quote(redirect_url)

    return template('async.tpl',
		{
                    'txt': txt,
                    'json': json.dumps(json_data),
                    'domain': domain,
                    'providerName' : json_data['providerName'], 
                    'asynchronousUrl': asynchronousUrl,
                    'asynchronousUrl3' : asynchronousUrl3,
                    'asynchronousUrl2' : asynchronousUrl2
                })                    
                    
# Handle the redirect back from the oAuth call
#
# Normally this would get the access token, store it, and then redirect to some other page on the client.
#
# Here we get the access token and simply return it to the client. The client will post it back to emulate 
# the async server call
@route("/async_oauth_response")
def async_oauth_response():

    host = request.headers['Host']

    # This only works for the hosting website
    if request.headers['Host'] != _hosting_website:
        return abort(404)

    # Get the data from the URL
    code = request.query.get("code")
    domain = request.query.get("domain")
    hosts = request.query.get("hosts")
    dns_provider = request.query.get('dns_provider')
    error = request.query.get('error')
    code_only = rquest.query.get('code_only')
    
    if error != None and error != '':
        return template('async_error',
                    {
                        'error': 'Error returned from DNSProvider (' + error + ')'
                    })

    if code_only != 1:

        # The original redirect url when getting the access token
        redirect_url = "http://" + _hosting_website + "/async_oauth_response?domain=" + domain + "&hosts=" + hosts + "&dns_provider=" + dns_provider

        # Take the oauth code and get an access token. This must be done fairly quickly as oauth codes have a short expiry
        url = oAuthAPIURLs[dns_provider] + "/v2/oauth/access_token?code=" + code + "&grant_type=authorization_code&client_id=" + _provider + "&client_secret=" + urllib.quote(oAuthSecrets[dns_provider]) + "&redirect_uri=" + urllib.quote(redirect_url)
        
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
            "code_only" : code_only,
            "code": code, 

            "domain": domain, 
            "hosts" : hosts, 
            "dns_provider": dns_provider,

            "access_token" : access_token, 
            "json_response": json_response, 

        })

# Handle the form post for the processing the asynchronous setting using an oAuth access token. 
@route("/async_confirm", method='POST')
def async_confirm():

    # This only works for the hosting website
    if request.headers['Host'] != _hosting_website:
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
    if domain == None or domain == '' or not _is_valid_hostname(domain) or message == None or message == '' or not _is_valid_message(message) or access_token == None or access_token == '' or dns_provider == None or dns_provider == '':
        return template('invalid_data.tpl')

    secs = calendar.timegm(time.gmtime()) # Seconds since the epoch

    # This is the URL to call the api to apply the template
    if 'template2' in request.forms.keys():
        url = oAuthAPIURLs[dns_provider] + '/v2/domainTemplates/providers/' + _provider + '/services/' + _template2 + '/apply?domain=' + domain + '&host=' + subdomain + '&force=' + str(force) + '&RANDOMTEXT=shm:' + str(secs) + ':' + message + '&IP=' + _ip
        applied_template = 'Template 2'
    else:
        url = oAuthAPIURLs[dns_provider] + '/v2/domainTemplates/providers/' + _provider + '/services/' + _template1 + '/apply?domain=' + domain + '&host=' + subdomain + '&force=' + str(force) + '&RANDOMTEXT=shm:' + str(secs) + ':' + message + '&IP=' + _ip
        applied_template = 'Template 1'

    # Call the api with the oauth acces bearer token

    r = requests.post(url, headers={'Authorization': 'Bearer ' + access_token}, verify=True)

    # If this fails, and there is a re-auth token, we could add this code here

    # Return a page. Normally you would store the access and re-auth tokens and redirect the client browser
    return template('async_confirm.tpl', 
        {"applied_template": applied_template,
         "message" : message,
         "access_token" : access_token, 
         "domain": domain, 
         "subdomain": subdomain,
         "hosts": hosts,
         "dns_provider" : dns_provider,
         "status_code" : str(r.status_code)
     })


# Gets the message text put into DNS for a domain name
def _get_messagetext(domain):
    try:
        messagetext = ''

        # Get the txt record for domain connect
        answers = dns.resolver.query(domain, 'TXT')
        timestamps = {}
        for answer in answers:
            data = answer.strings[0].split(':') # List containing ['shm', 'date', 'text']
            
            if data[0] == 'shm':
                if len(data) == 2:
                    data.insert(1, 0) # Resolves legacy issues wherein a user added an shm TXT record prior to timestamp support
                
                timestamps[data[1]] = data[2] # Add the date (seconds since epoch) and string to a Dictionary

        # Iterate through every timestamp, sorted
        sorted_dates = sorted(list(timestamps.keys()))
        for date in sorted_dates:
            messagetext += timestamps[date] + '<br>'

        return messagetext

    except:
        return None

# Get TXT records and parse them for the public key
def _get_publickey(domain):
    try:
        segments = {}
        publickey = '-----BEGIN PUBLIC KEY-----\n' # Key begins with prefix

        records = dns.resolver.query(domain, 'TXT') # Get all text records
        for text in records:
            split_text = text.strings[0].split(',') # Separate the index and key
            index = -1
            indexData = None
            for kv in split_text:
                parsed_kv = kv.split("=")
                key = parsed_kv[0]
                value = parsed_kv[1]
                if key == "p":
                    index = int(value)
                elif key == "d":
                    indexData = value
                elif key == "a" and value.upper() != "RS256":
                    return None
                elif key == "t" and value.lower() != "x509":
                    return None

            if index != -1 and indexData != None:
                segments[index] = indexData
        
        # Concatenate all of the key segments
        for key in sorted(segments.iterkeys()):
            publickey = publickey + segments[key]

        publickey += '\n-----END PUBLIC KEY-----' # Add suffix

        return publickey
    except:
        return None

# Checks if the DNS Provider supports our template
def _check_template(url):
    try:
        r = requests.get(url, verify=False)
        if r.status_code == 200:
           return True
        return False
    except:
        return False
    
# Checks if the DNS Provider supports Domain Connect
def _get_domainconnect_json(domain):

    try:
        # Get the txt record for domain connect from the domain
        answers = dns.resolver.query('_domainconnect.' + domain, 'TXT')
        if len(answers) != 1:
            return None, None

        # Get the value to do the json call
        host = answers[0].strings[0]

        # Form the URL to get the json and fetch it
        url = 'https://' + host + '/v2/' + domain + '/settings'
        r = requests.get(url, verify=False)
        return r.json(), host

    except:
        return None, None

# Generates a signature on the passed in data		
def _generate_sig(private_key, data):

    rsakey = RSA.importKey(private_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(data)

    return b64encode(signer.sign(digest))

# Verifies a sinature
def _verify_sig(public_key, signature, data):

    rsakey = RSA.importKey(public_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(data)

    if signer.verify(digest, b64decode(signature)):
        return True

    return False

# Valid host names pass simple domain name validation
def _is_valid_hostname(hostname):
    if len(hostname) < 4 or len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

# A valid message can only contain certain characters
def _is_valid_message(message):
    if len(message) < 1 or len(message) > 255:
        return False
    return re.match("^[a-zA-Z ,.?!0-9]*$", message) is not None

@route('/static/<filename>')
def send_static(filename):
    return static_file(filename, root='static')

# Runs the application for all hosts
if __name__ == "__main__":
    run(host='0.0.0.0', port=80, debug=True)

