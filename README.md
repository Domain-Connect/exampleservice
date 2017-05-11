# python-dc-statelesshosting

# This simple application implements "stateless hosting". This is hosting a web page for a domain with no server state.
# 
# The page rendered for a domain simply displays the host (domain) name and simple message configurable by the user. The message
# is cleverly stored in DNS, allowing fo the "stateless" claim.
#
# DNS for a domain hosted on this platform requires two records.  One for an the A Record's IP address. The other for for a TXT
# record containing the message.
#
# The application asks for a domain name and message. Once input, the application runs Domain Connect to first discover
# the identity of the DNS Provider, and then to configure the two values in DNS.
#
# The implementation of this is purposefully simple and low fidelity to clearly demonstrate the Domain Connect flow.
