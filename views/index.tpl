% include('header.tpl', title='DC Example Service')

<h1>Example Service Provider</h1>
This website demonstrates a sample Domain Conect Service Provider.
<p/>
The service hosts a website, displaying a custom message to the user. Like many hosting SaaS providers, this service requires modifications to DNS in the form of an A Record. It also stores the custom message in DNS in a TXT record. This is rather clever, using DNS as a distributed database. But wouldn't be advocated in a real world applications.
<p/>
There are two templates as part of this application. Both setup the service is slightly different ways. The first template sets up DNS as described above. The second adds an additional CNAME, and requires signatures.
<p/>
<a target=_template1 href="https://github.com/Domain-Connect/Templates/blob/master/exampleservice.domainconnect.org.template1.json">Template 1</a>
<p/>
<a target=_template2 href="https://github.com/Domain-Connect/Templates/blob/master/exampleservice.domainconnect.org.template2.json">Template 2</a>

<h2>Synchronous</h2>
For the synchronous protocol, we need the domain name, the optional host (subdomain), and the message. The subsequent page will form the URL to apply one of the two tempaltes.
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
For the asynchronous protocol, we need the domain name and the message as per above. We also need the list of hosts (including empty for the root). Examples:
<p/>
<table border=1 cellpadding=3>
<tr><td>Domain Name</td><td>Host</td><td>Valid domains for asynchronous template application</td></tr>
<tr><td>foo.com</td><td></td><td>foo.com</td></tr>
<tr><td>foo.com</td><td>bar</td><td>bar.foo.com</td></tr>
<tr><td>foo.com</td><td>bar1,bar2,</td><td>foo.com|bar1.foo.com|bar2.foo.com</td></tr>
</table>
<p/>
The subsequent pages will get permission and allow application of template1 or template2.
<p/>
<form method="post" action='/async'>
<table>
<tr><td>Domain Name</td><td><input name='domain' type="text"/></td></tr>
<tr><td>Host (optional)</td><td><input name='hosts' type="text"/></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Configure Async" /></td></tr>
</table>
</form>

% include('footer.tpl')

