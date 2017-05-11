from bottle import Bottle, run, route, template, request, response, abort
from dns.resolver import dns
import requests
import json
import re

# This simple application implements "stateless hosting". This is hosting a web page for a domain with no server state.
# 
# The page rendered for a domain simply displays the host (domain) name and simple message configurable by the user. The message
# is cleverly stored in DNS, allowing fo the "stateless" claim.
#
# DNS for a domain hosted on this platform requires two records.  One for an the A Record's IP address. The other for for a TXT
# record containing the message.
#
# The implementation of this is purposefully simple and low fidelity to clearly demonstrate the Domain Connect flow.


# This is the IP address of the server I'm running this sample code
_ip = '10.32.44.84'

# This is the name of the application where users configure their sites
_hosting_website = 'statelesshosting.com'

# Handle the home page. This can be rendered for the service, or the individual sites
@route('/')
def index():

    # Get the host name
    host = request.headers['Host']

    # If the host is my hosting website, render the home page
    if host == _hosting_website:
        return template('index.tpl', {})

    # See if the text string was put into DNS
    messagetext = _get_messagetext(host)

    # We only render a site for domains that have been configured with a message
    if messagetext == None or messagetext == '':
        return abort(404)

    # Render the site 
    return template('site.tpl', {'host': request.headers['Host'], 'messagetext': messagetext})

# The form post of the domain name and the message come here
@route('/configure', method='POST')
def configure():

    host = request.headers['Host']

    # This only works for the hosting website
    if host != _hosting_website:
        return abort(404)

    # Get the domain anme and the message and validate
    domain = request.forms.get('domain')
    message = request.forms.get('message')
    if domain == None or domain == '' or not _is_valid_hostname(domain) or message == None or message == '' or not _is_valid_message(message):
        return template('invalid_data.tpl')

    # See if the DNS Provider supports domain connect
    json_data = _get_domainconnect_json(domain)
    if json_data == None:
        return template('no_domain_connect.tpl')

    # Create the URL to oonfigure with domain connect
    #
    # This sample service provider (whdhackathon) and service template (whd-template-1) were created for a hackathon in 2017. This can be used to test services across providers
    #
    # This template takes two variables. The IP address for the A Record (IP=), and string put into a TXT record (RANDOMTEXT=)
    targetUrl = json_data['urlSyncUX'] + '/v2/domainTemplates/providers/whdhackathon/services/whd-template-1/apply?domain=' + domain + '&RANDOMTEXT=shm:' + message + '&IP=' + _ip

    # Render the confirmation page
    return template('confirm.tpl', {'domain': domain, 'providerName' : json_data['providerName'], 'targetUrl' : targetUrl})

def run_all():
    run(host='0.0.0.0', port=80, debug=True)

# Gets the message text put into DNS for a domain name
def _get_messagetext(domain):
    try:
        messagetext = None

        # Get the txt record for domain connect
        answers = dns.resolver.query(domain, 'TXT')
        for i in range(len(answers)):
            answer = answers[i].strings[0]
            
            if answer.startswith('shm:'):
                messagetext = answer[4:]

        return messagetext

    except:
        return None

def _get_domainconnect_json(domain):

    try:
        # Get the txt record for domain connect
        answers = dns.resolver.query('_domainconnect.' + domain, 'TXT')
        if len(answers) != 1:
            return None

        # Get the host name
        host = answers[0].strings[0]

        # Form the URL to get the json and fetch it
        url = 'https://' + host + '/v2/' + domain + '/settings'
        r = requests.get(url, verify=False)
        return r.json()

    except:
        return None

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
