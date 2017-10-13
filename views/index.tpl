% include('header.tpl', title='DC Example Service')
<h1>Example Service Provider</h1>
<h2>This website demonstrates a sample Domain Connect Service Provider. You enter your domain name, subdomain (optional) and a message to display. Using Domain Connect, these values are places in DNS which are used to later render the message entered as the site content for the domain/subdomain.</h2>

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
