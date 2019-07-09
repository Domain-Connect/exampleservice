% include('header.tpl', title='DC Example Service')

<h2>Synchronous Detailed</h2>
This flow will show detailed steps of the synchronous protocol, and is intended for the developer. The end result is the same as the <a href='/simple_index'>Simple Flow</a>.
<p/>
Input your message, and enter the domain and optional sub-domain (host) for your new Website.
<p/>
<form method="post" action='/sync_post'>
<table>
<tr><td>Message</td><td><input name='message' type="text"/></td></tr>
<tr><td>--</td><td></td></tr>
<tr><td>Domain Name</td><td><input name='domain' type="text"/></td></tr>
<tr><td>Host (optional)</td><td><input name='subdomain' type="text"/></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Configure Sync" /></td></tr>
</table>
</form>

% include('footer.tpl')
