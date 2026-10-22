% include('header.tpl', title='DC Example Service')

<h2>Asynchronous</h2>
This flow will show the detailed steps of the asynchronous (OAuth based) protocol, and is intended for the developer.
<p/>
Hosts is a list of comma delimted host names. An empty value allows the root domain.
<h4>Example Host Parameters</h4>
<table border=1 cellpadding=3>
<tr><th>Domain Name</th><th>Hosts</th><th>Valid fully qualified domain names for template application</th></tr>
<tr><td>foo.com</td><td></td><td>foo.com</td></tr>
<tr><td>foo.com</td><td>bar</td><td>bar.foo.com</td></tr>
<tr><td>foo.com</td><td>bar1,bar2,</td><td>foo.com|bar1.foo.com|bar2.foo.com</td></tr>
</table>
<p/>
The subsequent pages will get permission, and then allow application of template1 or template2 on domain/host tuples via the API. The message for the site is provided there.
<p/>
<form method="post" action='/async_post'>
<table>
<tr><td>Domain Name</td><td><input name='domain' type="text"/></td></tr>
<tr><td>Host (optional)</td><td><input name='hosts' type="text"/></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Configure Async" /></td></tr>
</table>
</form>


% include('footer.tpl')
