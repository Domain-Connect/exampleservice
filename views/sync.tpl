% include('header.tpl', title='Configure Domain Connect')

<h1>Provider Found: Your domain uses {{providerName}}</h1>
The query for the _domainconnect TXT record returned: {{txt}}
<p/>
The json returned by https://{{txt}}/v2/{{domain}}/settings: {{json}}

<h2>New Tab</h2>
<a target=_new href='{{synchronousUrl1}}'>Configure Template 1</a>
<p/>
<a target=_new href='{{synchronousSignedUrl2}}'>Configure Template 2 Synchronously with Signature Verification</a>
<form method="post" action="sig_verify">
<input name="domain" type="hidden" value="exampleservice.domainconnect.org">
<input name="key" type="hidden" value="_dck1">
<input name="sig" type="hidden" value="{{sig}}">
<input name="qs" type="hidden" value="{{qs}}">
<input type="submit" value="Verify Signature" />
</form>

<h2>New Window</h2>
<a target=_new href='javascript:null(void);' onclick='window.open("{{synchronousUrl1}}", "", "width={{width}},height={{height}}");'>Configure Template 1</a>
<p/>
<a target=_new href='javascript:null(void);' onclick='window.open("{{synchronousSignedUrl2}}", "", "width={{width}},height={{height}}");'>Configure Template 2 Synchronously with Signature Verification</a>
<form method="post" action="sig_verify">
<input name="domain" type="hidden" value="exampleservice.domainconnect.org">
<input name="key" type="hidden" value="_dck1">
<input name="sig" type="hidden" value="{{sig}}">
<input name="qs" type="hidden" value="{{qs}}">
<input type="submit" value="Verify Signature" />
</form>

<h2>In Place w/ Redirect</h2>
<a href='{{synchronousRedirectUrl1}}'>Configure Template 1</a>
<p/>
<a href='{{synchronousSignedRedirectUrl2}}'>Configure Template 2 Synchronously with Signature Verification</a>
<form method="post" action="sig_verify">
<input name="domain" type="hidden" value="exampleservice.domainconnect.org">
<input name="key" type="hidden" value="_dck1">
<input name="sig" type="hidden" value="{{sigRedirect}}">
<input name="qs" type="hidden" value="{{qsRedirect}}">
<input type="submit" value="Verify Signature" />
</form>

% include('footer.tpl')

