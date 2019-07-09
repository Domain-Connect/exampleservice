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

<h4>Step 4<h4>
URL to call and start oAuth process

<pre style=font-family:courier; word-break:break-all">
{{asynchronousUrl}}
</pre>

<h2>Next Step</h2>


<p style="font-family:courier; word-break:break-all">{{asynchronousUrl}}</p>
<p/>
Provider Found: Your domain uses {{providerName}}. 
<p/>
<a href='{{asynchronousUrl}}'>Get Asynchronous Permission</a>

% include('footer.tpl')

