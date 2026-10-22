% include('header.tpl', title='Client Side')

<script src='/static/domainconnect.js'>
</script>

<script>

function callbackfunc(url, domain, host, provider_name, data) {
    if (url) {
        url = url + '&RANDOMTEXT=shm:0:' + encodeURIComponent(data) + '&IP=132.148.166.208'

	document.getElementById("domainconnect").innerHTML = "<h1>Results</h1>Click to <a target=_new href='" + url + "'>configure</a> your domain with " + provider_name
	
    } else {
        document.getElementById('domainconnect').innerHTML = "<h1>Results</h1)Domain does not support domain connect";
    }
		 
	 
}

function publish() {
	 domain = document.getElementById('domain').value;
	 message = document.getElementById('message').value;
	 host = document.getElementById('host').value;

	 domain_connect(domain, host, message, 'exampleservice.domainconnect.org', 'template1', callbackfunc);
}
</script>

<h2>Client Side</h2>
This will demonstrate the use of the synchronous protocol, but entirely from the context of client (no server). This only works for
templates that are synchronous and do NOT require a signature. For the example service, this is template1 (template2 requires a
signature.

<table>
<tr><td>Message:</td><td><input name='message' type='text' id='message'/></td></tr>
<tr><td>--</td><td></td></tr>
<tr><td>Domain Name</td><td><input name='domain' type="text" id='domain'/></td></tr>
<tr><td>Host (optional)</td><td><input name='subdomain' type="text" id='host'/></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Publish" onclick="publish();"/></td></tr>
</table>

<div id="domainconnect">
</div>

% include('footer.tpl')

