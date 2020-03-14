import dns.resolver

import re

import calendar
import time

import requests

def dns_message_data(message):
    secs = calendar.timegm(time.gmtime())
    return 'shm:' + str(secs) + ':' + message

# Valid host names pass simple domain name validation
def is_valid_hostname(hostname):
    if len(hostname) < 4 or len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

# A valid message can only contain certain characters
def is_valid_message(message):
    if len(message) < 1 or len(message) > 255:
        return False
    return re.match("^[a-zA-Z ,.?!0-9]*$", message) is not None

# Gets the message text put into DNS for a domain name
def get_messagetext(domain):
    try:
        messagetext = ''

        # Get the txt record for domain connect
        answers = dns.resolver.query(domain, 'TXT')
        timestamps = {}
        for answer in answers:
            data = answer.strings[0].decode("utf-8").split(':') # List containing ['shm', 'date', 'text']
            
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

# Checks if the DNS Provider supports our template
def check_template(url):
    try:
        r = requests.get(url, verify=False)
        if r.status_code == 200:
           return True
        return False
    except:
        return False
    
    
# Checks if the DNS Provider supports Domain Connect
def get_domainconnect_json(domain):

  try:

    # Get the txt record for domain connect from the domain
    answers = dns.resolver.query('_domainconnect.' + domain, 'TXT')
    if len(answers) != 1:
        return None, None, 'No _domainconnect TXT record'

    # Get the value to do the json call
    host = answers[0].strings[0].decode('utf-8')

    # Form the URL to get the json and fetch it
    url = 'https://' + host + '/v2/' + domain + '/settings'
    r = requests.get(url, verify=False)

    # Remember that the json might fail if the provider from the DNS TXT record doesn't contain the zone
    if r.status_code != 200:
        return None, None, 'No json returned for /settings'

    # Get the json
    json_data = r.json()

    # If the provider returned nameservers, verify that they are athoritative
    if 'nameServers' in json_data:
        answers = dns.resolver.query(domain, 'NS')
        if len(answers) == 0:
            return None, None, 'No nameservers found'
        authoritative = str(answers[0])
        if authoritative.endswith('.'):
            authoritative = authoritative[:-1]
        if len(answers) == 0 or authoritative not in json_data['nameServers']:
            return None, None, 'Nameservers not authoritative'

    return json_data, host, None

  except:
    return None, None, 'Internal error'

    
