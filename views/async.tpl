% include('header.tpl', title='Configure Domain Connect')

<h1>Provider Found: Your domain uses {{providerName}}</h1>
The query for the _domainconnect TXT record returned: {{txt}}
<p/>
The json returned by https://{{txt}}/v2/{{domain}}/settings: {{json}}
<p/>
<a href='{{asynchronousUrl}}'>Configure Asynchronously: Obsolete with service in path</a>
<p/>
<a href='{{asynchronousUrl3}}'>Configure Asynchronously (Code Only): Obsolete with service in path</a>
<p/>
<a href='{{asynchronousUrl2}}'>Configure Asynchronously: Current spec without service in path</a>
<p/>
NOTE: The spec was updated to remove the service from the path, as this is now specified in the scope. Some older providers are still updating.
% include('footer.tpl')

