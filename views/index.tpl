% include('header.tpl', title='DC Example Service')

<h2>Example Service Provider</h2>
This serice demonstrates a sample Domain Conect Service Provider.
<p/>
The service hosts a website for a domain name that displays a custom message. Like many hosting SaaS providers, this service requires modifications to DNS in the form of an A Record. It also happens to store the custom message in DNS in a TXT record. This is rather clever, as it is using DNS as a distributed database. While we would not advocate this in a real world application, it allows for a simple example application that requires no state data.
<p/>
The application also demonstrates two templates. The first template sets up DNS as described above. The second adds an additional CNAME, and requires signatures. Like all templates, these can be found on github.
<p/>
<p>
<a target=_template1 href="https://github.com/Domain-Connect/Templates/blob/master/exampleservice.domainconnect.org.template1.json">Template 1</a>
<p/>
<a target=_template2 href="https://github.com/Domain-Connect/Templates/blob/master/exampleservice.domainconnect.org.template2.json">Template 2</a>
<p>
Domain Connect works in one of two ways. One is synchronous and one is asynchronous using oauth.

<h2>Synchronous</h2>
For the synchronous protocol, we need the domain name, the optional host (subdomain), and the message. The subsequent page will detect the DNS Provider and provide links to apply the template.
<p/>
<form method="post" action='/sync'>
<table>
<tr><td>Domain Name</td><td><input name='domain' type="text"/></td></tr>
<tr><td>Host (optional)</td><td><input name='subdomain' type="text"/></td></tr>
<tr><td>Message</td><td><input name='message' type="text"/></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Configure Sync" /></td></tr>
</table>
</form>

<h2>Asynchronous</h2>
For the asynchronous protocol, we need the domain name and the hosts. These are the hosts (sub-domains) upon which the template can be applied programatically later. There is no message collected here, because this is input to the API later.
<p/>
Hosts is a list of comma delimted host names. An empty value allows the root domain.
<h3>Example Parameters</H3>
<table border=1 cellpadding=3>
<tr><th>Domain Name</th><th>Hosts</th><th>Valid fully qualified domain names for template application</th></tr>
<tr><td>foo.com</td><td></td><td>foo.com</td></tr>
<tr><td>foo.com</td><td>bar</td><td>bar.foo.com</td></tr>
<tr><td>foo.com</td><td>bar1,bar2,</td><td>foo.com|bar1.foo.com|bar2.foo.com</td></tr>
</table>
<p/>
The subsequent pages will get permission, and then allow application of template1 or template2 on domain/host tuples via the API.
<p/>
<form method="post" action='/async'>
<table>
<tr><td>Domain Name</td><td><input name='domain' type="text"/></td></tr>
<tr><td>Host (optional)</td><td><input name='hosts' type="text"/></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Configure Async" /></td></tr>
</table>
</form>

% include('footer.tpl')

