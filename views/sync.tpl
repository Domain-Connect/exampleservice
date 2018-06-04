% include('header.tpl', title='Configure Domain Connect')

<h2>Provider Found: Your domain uses {{providerName}}</h2>
<table border=1 cellpadding=3>
<tr><td>_domainconnect TXT record at {{domain}}</td><td>{{txt}}</td></tr>
<tr><td>json returned by https://{{txt}}/v2/{{domain}}/settings</td><td>{{json}}</td></tr>
<tr><td>URL to query for support for template 1</td><td>{{check_url1}}</td></tr>
<tr><td>URL to query for support for template 2</td><td>{{check_url2}}</td></tr>
<tr><td>URL to apply template 1</td><td>{{synchronousUrl1}}</td></tr>
<tr><td>URL to apply template 2 with signature</td><td>{{synchronousSignedUrl2}}</td></tr>
</table>

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

