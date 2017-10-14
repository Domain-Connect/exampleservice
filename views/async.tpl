% include('header.tpl', title='Configure Domain Connect')

<h1>Provider Found: Your domain uses {{providerName}}</h1>
The query for the _domainconnect TXT record returned: {{txt}}
<p/>
The json returned by https://{{txt}}/v2/{{domain}}/settings: {{json}}
<p/>
<a href='{{asynchronousUrl}}'>Configure Asynchronously</a>

%include('footer.tpl')
