% include('header.tpl', title='Configure Domain Connect')

<h1>Provider Found: Your domain uses {{providerName}}</h1>
The query for the _domainconnect TXT record returned: {{txt}}
<p/>
The json returned by https://{{txt}}/v2/{{domain}}/settings: {{json}}
<p/>
<a target=_new href='{{synchronousUrl1}}'>Configure Template 1 Synchronously</a>
<p/>
<a target=_new href='{{synchronousUrl2}}'>Configure Template 2 Synchronously</a>
<p/>
<a target=_new href='{{synchronousSignedUrl1}}'>Configure Template 1 Synchronously with Signature Verification</a> (Verified = {{verified}})
<p/>
<a target=_new href='{{synchronousSignedUrl2}}'>Configure Template 2 Synchronously with Signature Verification</a> (Verified = {{verified}})
<p/>
<a href='{{synchronousRedirectUrl1}}'>Configure Template 1 Inline Synchronously</a>
<p/>
<a href='{{synchronousRedirectUrl2}}'>Configure Template 2 Inline Synchronously</a>
<p/>
<a href='{{synchronousSignedRedirectUrl1}}'>Configure Template 1 Inline Synchronously with Signature Verification</a> (Verified = {{verifiedRedirect}})
<p/>
<a href='{{synchronousSignedRedirectUrl2}}'>Configure Template 2 Inline Synchronously with Signature Verification</a> (Verified = {{verifiedRedirect}})


%include('footer.tpl')
