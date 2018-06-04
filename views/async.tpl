% include('header.tpl', title='Configure Domain Connect')

<h2>Provider Found: Your domain uses {{providerName}}</h2>

<table border=1 cellpadding=3>
<tr><td>_domainconnect TXT record at {{domain}}</td><td>{{txt}}</td></tr>
<tr><td>json returned by https://{{txt}}/v2/{{domain}}/settings</td><td>{{json}}</td></tr>
<tr><td>URL to query for support for template 1</td><td>{{check_url1}}</td></tr>
<tr><td>URL to query for support for template 2</td><td>{{check_url2}}</td></tr>
<tr><td>URL for getting oAuth permission (obsolete with service in path)</td><td>{{asynchronousUrl}}</td></tr>
<tr><td>URL for getting oAuth permission</td><td>{{asynchronousUrl2}}</td></tr>
</table>

<p/>
<a href='{{asynchronousUrl}}'>Configure Asynchronously: Obsolete with service in path</a>
<p/>
<a href='{{asynchronousUrl2}}'>Configure Asynchronously: Current spec without service in path</a>
<p/>
NOTE: The spec was updated to remove the service from the path, as this is now specified in the scope. Some older providers are still updating.
% include('footer.tpl')

