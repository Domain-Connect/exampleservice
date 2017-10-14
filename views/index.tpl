% include('header.tpl', title='DC Example Service')
<h1>Example Service Provider</h1>
<h2>Instructions</h2>
This website demonstrates a sample Domain Connect Service Provider. The service can host a website, displaing a custom message. This application uses two templates.
<p/>
<a target=_template1 href="https://github.com/Domain-Connect/Templates/blob/master/exampleservice.domainconnect.org.template1.json">Template 1</a>
<p/>
<a target=_template2 href="https://github.com/Domain-Connect/Templates/blob/master/exampleservice.domainconnect.org.template2.json">Template 2</a>

<h2>Synchronous</h2>
<form method="post" action='/sync'>
<table>
<tr><td>Domain Name</td><td><input name='domain' type="text"/></td></tr>
<tr><td>Sub-Domain (optional)</td><td><input name='subdomain' type="text"/></td></tr>
<tr><td>Message</td><td><input name='message' type="text"/></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Configure Sync" /></td></tr>
</table>
</form>

<h2>Asynchronous</h2>
<form method="post" action='/async'>
<table>
<tr><td>Domain Name</td><td><input name='domain' type="text"/></td></tr>
<tr><td>Hosts (optional)</td><td><input name='hosts' type="text"/></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Configure Async" /></td></tr>
</table>
</form>

%include('footer.tpl')
