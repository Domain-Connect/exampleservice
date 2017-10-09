% include('header.tpl', title='Configure Domain Connect')
<h1>Provider Found</h1>
The query for the _domainconnect TXT record returned: {{host}}
<p/>
The json returned by https://{{host}}/v2/{{domain}}/settings: {{json}}
Your domain uses {{providerName}}
<p/>
<a target=_new href='{{synchronousTargetUrl1}}'>Configure Synchronously</a>
<p/>
<a target=_new href='{{synchronousTargetUrl2}}'>Configure Synchronously (alternative template)</a>
<p/>
<a target=_new href='{{synchronousSignedTargetUrl1}}'>Configure Synchronously with Signature verification (not supported by all providers)</a> (Verified = {{verified}})
<p/>
<a target=_new href='{{synchronousSignedTargetUrl2}}'>Configure Synchronously (alternative template) with Signature verification (not supported by all providers)</a> (Verified = {{verified}})
<p/>
% if asynchronousTargetUrl != None:
    <a href='{{asynchronousTargetUrl}}'>Configure Asynchronously</a>
% else:
    Async not supported by provider
% end
%include('footer.tpl')
