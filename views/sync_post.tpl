% include('header.tpl', title='Configure Domain Connect')

<h2>Discovering the DNS Provider<h2>

<h4>Step 1</h4>
Query for the _domainconnect TXT record at {{domain}}:
<p/>
<p style="font-family:courier; word-break:break-all">{{txt}}</p>

<h4>Step 2</h4>
Calling URL https://{{txt}}/v2/{{domain}}/settings:
<p/>
<pre style="font-family:Courier" id="json"></pre>
<script>document.getElementById("json").innerHTML = JSON.stringify({{!json}}, undefined, 2);</script>

<h4>Step 3</h4>
URLs to query for support of templates:
<p/>
<p style="font-family:courier; word-break:break-all">{{check_url1}}</p>
<p/>
<p style="font-family:courier; word-break:break-all">{{check_url2}}</p>

<h4>Step 4</h4>
URL to call domain connect for template 1

<pre style="font-family:courier; word-break:break-all">
{{synchronousUrl1}}
</pre>

<h2>Next Step</h2>
<h4>New Tab</h4>
<a target=_new href='{{synchronousUrl1}}'>Configure Template 1</a>
<p/>
<a target=_new href='{{synchronousSignedUrl2}}'>Configure Template 2 with Signature Verification</a>
<form method="post" action="sig_verify">
<input name="domain" type="hidden" value="exampleservice.domainconnect.org">
<input name="key" type="hidden" value="_dck1">
<input name="sig" type="hidden" value="{{sig}}">
<input name="qs" type="hidden" value="{{qs}}">
<input type="submit" value="Verify Signature" />
</form>

<h4>New Window</h4>
<a target=_new href='javascript:null(void);' onclick='window.open("{{synchronousUrl1}}", "", "width={{width}},height={{height}}");'>Configure Template 1</a>
<p/>
<a target=_new href='javascript:null(void);' onclick='window.open("{{synchronousSignedUrl2}}", "", "width={{width}},height={{height}}");'>Configure Template 2 with Signature Verification</a>
<form method="post" action="sig_verify">
<input name="domain" type="hidden" value="exampleservice.domainconnect.org">
<input name="key" type="hidden" value="_dck1">
<input name="sig" type="hidden" value="{{sig}}">
<input name="qs" type="hidden" value="{{qs}}">
<input type="submit" value="Verify Signature" />
</form>

<h4>In Place w/ Redirect</h4>
<a href='{{synchronousRedirectUrl1}}'>Configure Template 1</a>
<p/>
<a href='{{synchronousSignedRedirectUrl2}}'>Configure Template 2 with Signature Verification</a>
<form method="post" action="sig_verify">
<input name="domain" type="hidden" value="exampleservice.domainconnect.org">
<input name="key" type="hidden" value="_dck1">
<input name="sig" type="hidden" value="{{sigRedirect}}">
<input name="qs" type="hidden" value="{{qsRedirect}}">
<input type="submit" value="Verify Signature" />
</form>

% include('footer.tpl')

