% include('header.tpl', title='Configure Domain Connect')

<h1>Provider Found: Your domain uses {{providerName}}</h1>
The query for the _domainconnect TXT record at {{domain}} returned: <b>{{txt}}</b>
<p/>
The json returned by https://{{txt}}/v2/{{domain}}/settings:<br/> <b>{{json}}</b>
<p/>
The query for support for template 1 at {{check_url1}} returned: <b>200 OK</b>
<p/>
The query for support for template 2 at {{check_url2}} returned: <b>200 OK</b>
<p/>
The URL for getting oAuth (obsolete with service in path): <b>{{asynchronousUrl}}</b>
<p/>
The URL for getting oAuth: <b>{{asynchronousUrl2}}</b>
<p/>
<a href='{{asynchronousUrl}}'>Configure Asynchronously: Obsolete with service in path</a>
<p/>
<a href='{{asynchronousUrl2}}'>Configure Asynchronously: Current spec without service in path</a>
<p/>
NOTE: The spec was updated to remove the service from the path, as this is now specified in the scope. Some older providers are still updating.
% include('footer.tpl')

