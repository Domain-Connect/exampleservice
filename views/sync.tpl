% include('header.tpl', title='Configure Domain Connect')

<h1>Provider Found: Your domain uses {{providerName}}</h1>
The query for the _domainconnect TXT record returned: {{txt}}
<p/>
The json returned by https://{{txt}}/v2/{{domain}}/settings: {{json}}
<p/>
<a target=_new href='{{synchronousTargetUrl1}}'>Configure Synchronously</a>
<p/>
<a target=_new href='{{synchronousTargetUrl2}}'>Configure Synchronously (alternative template)</a>
<p/>
<a target=_new href='{{synchronousSignedTargetUrl1}}'>Configure Synchronously with Signature verification (not supported by all providers)</a> (Verified = {{verified}})
<p/>
<a target=_new href='{{synchronousSignedTargetUrl2}}'>Configure Synchronously (alternative template) with Signature verification (not supported by all providers)</a> (Verified = {{verified}})

%include('footer.tpl')
