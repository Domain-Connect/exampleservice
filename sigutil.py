from dns.resolver import dns

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode, b64encode,urlsafe_b64decode,b16encode

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

# Get TXT records and parse them for the public key
def get_publickey(domain):
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


