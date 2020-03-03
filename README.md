# Stateless Hosting

This simple application implements "stateless hosting". This is hosting a web page for a domain with no server state.
 
The page rendered for a domain simply displays the host (domain) name and simple message configurable by the user. The message
is cleverly stored in DNS, allowing for the "stateless" claim.

DNS for a domain hosted on this platform requires two records.  One for an A Record's IP address. The other for a TXT
record containing the message.

The application asks for a domain name and message. Once input, the application runs Domain Connect to first discover
the identity of the DNS Provider, and then to configure the two values in DNS.

The implementation of this is purposefully simple and low fidelity to clearly demonstrate the Domain Connect flow.

# Implementation

This is a simple Python bottle application. To run, install python. Also, pip install bottle.

There are two lines in the file you'll want to change. The first is the IP address for the server. The second is domain name of your
application.

Run python and import statelesshosting.py (from statelesshosting import *).

Then use the command "run_all()". This will run the bottle development server on port 80 (you'll need root privilage to do this).

# Accessing the app

This application runs at exampleservice.domainconnect.org.

# Run locally

You can also run this application locally on your own box in a simple bottle server.  Just sudo python statelesshosting.py.

One caveat: you'll need to modify your local hosts file so exampleservice.domainconnect.org resolves to your own localhost.

Also see instructions on running in [Docker](docker/README.md).

# Dependencies

The service uses python3.

It relies on bottle, dnspython, cryptography, and the requests packages.