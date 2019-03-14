import re

from dns.resolver import dns

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode, b64encode,urlsafe_b64decode,b16encode

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
def get_publickey(domain):
    try:
        segments = {}

        pembits = ''

        records = dns.resolver.query(domain, 'TXT') # Get all text records
        record_strings = []
        for text in records:
            record_strings.append(str(text))
            split_text = text.strings[0].split(',') # Separate the components
            index = -1
            indexData = None
            for kv in split_text:
                if kv.startswith('p='):
                    index = int(kv[2:])
                elif kv.startswith('d='):
                    indexData = kv[2:]
                elif kv.startswith('a=') and kv != 'a=RS256':
                    return None, None
                elif kv.startswith('t=') and kv != 't=x509':
                    return None, None

            if index != -1 and indexData != None:
                segments[index] = indexData

        # Concatenate all of the key segments
        for key in sorted(segments.iterkeys()):
            pembits = pembits + segments[key].strip('\n').strip('\\n').strip()
            
        return pembits, record_strings
    except:
        return None, None

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

    
        # Get the txt record for domain connect from the domain
        answers = dns.resolver.query('_domainconnect.' + domain, 'TXT')
        if len(answers) != 1:
            return None, None

        # Get the value to do the json call
        host = answers[0].strings[0]

        # Form the URL to get the json and fetch it
        url = 'https://' + host + '/v2/' + domain + '/settings'
        r = requests.get(url, verify=False)

        # Remember that the json might fail if the provider from the DNS TXT record doesn't contain the zone
        if r.status_code != 200:
            return None, None

        return r.json(), host

    
# Generates a signature on the passed in data		
def generate_sig(private_key, data):

    rsakey = RSA.importKey(private_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(data)

    return b64encode(signer.sign(digest))

# Verifies a sinature
def verify_sig(public_key, signature, data):

    rsakey = RSA.importKey(public_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(data)

    if signer.verify(digest, b64decode(signature)):
        return True

    return False


