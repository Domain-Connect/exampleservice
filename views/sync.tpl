% include('header.tpl', title='Configure Domain Connect')

<h1>Provider Found: Your domain uses {{providerName}}</h1>
The query for the _domainconnect TXT record returned: {{txt}}
<p/>
The json returned by https://{{txt}}/v2/{{domain}}/settings: {{json}}
<p/>
Signature Verified: {{verified}}
<p/>
Redirect Signature Verified: {{verifiedRedirect}}
<h2>New Tab</h2>
<a target=_new href='{{synchronousUrl1}}'>Configure Template 1</a>
<p/>
<a target=_new href='{{synchronousSignedUrl2}}'>Configure Template 2 Synchronously with Signature Verification</a>
<h2>New Window</h2>
<a target=_new href='javascript:null(void);' onclick='window.open("{{synchronousUrl1}}", "", "width={{width}},height={{height}}");'>Configure Template 1</a>
<p/>
<a target=_new href='javascript:null(void);' onclick='windowopen("{{synchronousSignedUrl2}}", "", "width={{width}},height={{height}}");'>Configure Template 2 Synchronously with Signature Verification</a>
<h2>In Place w/ Redirect</h2>
<a href='{{synchronousRedirectUrl1}}'>Configure Template 1</a>
<p/>
<a href='{{synchronousSignedRedirectUrl2}}'>Configure Template 2 Synchronously with Signature Verification</a>


%include('footer.tpl')
