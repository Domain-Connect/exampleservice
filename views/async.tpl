% include('header.tpl', title='Configure Domain Connect')

<h2>Provider Found: Your domain uses {{providerName}}</h2>

<table border=1 cellpadding=3>
<tr><td>_domainconnect TXT record at {{domain}}</td><td>{{txt}}</td></tr>
<tr><td>json returned by https://{{txt}}/v2/{{domain}}/settings</td><td>{{json}}</td></tr>
<tr><td>URL to query for support for template 1</td><td>{{check_url1}}</td></tr>
<tr><td>URL to query for support for template 2</td><td>{{check_url2}}</td></tr>
<tr><td>URL for getting oAuth permission</td><td>{{asynchronousUrl}}</td></tr>
</table>

<p/>
<a href='{{asynchronousUrl}}'>Get Asynchronous Permission</a>

% include('footer.tpl')

