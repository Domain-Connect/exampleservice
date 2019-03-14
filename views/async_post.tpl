% include('header.tpl', title='Configure Domain Connect')

<h2>Discovering the DNS Provider<h2>

<h4>Step 1</h4>
Query for the _domainconnect TXT record at {{domain}}:
<p/>
<p style="font-family:courier; word-break:break-all">{{txt}}</p>

<h4>Step 2</h4>
json returned by https://{{txt}}/v2/{{domain}}/settings:
<p/>
<pre style="font-family:Courier" id="json"></pre>
<script>document.getElementById("json").innerHTML = JSON.stringify({{!json}}, undefined, 2);</script>

<h4>Step 3</h4>
URLs to query for support of templates:
<p/>
<p style="font-family:courier; word-break:break-all">{{check_url1}}</p>
<p/>
<p style="font-family:courier; word-break:break-all">{{check_url2}}</p>

<h2>Next Step</h2>

URL for getting oAuth permission:
<p/>
<p style="font-family:courier; word-break:break-all">{{asynchronousUrl}}</p>
<p/>
Provider Found: Your domain uses {{providerName}}. The following URL will
ask for permissions to apply template1 and template2 on {{domain}} with hosts [{{hosts}}].
<p/>
<a href='{{asynchronousUrl}}'>Get Asynchronous Permission</a>

% include('footer.tpl')

