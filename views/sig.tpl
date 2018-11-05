% include('header.tpl', title='Signature Verification')

<h1>Signatures</h1>
Signatures are sometimes needed when using the sycnrhonous protocol. Signatures
are needed if your
template has variables that could be replaced by malicious values by a bad 
actor (say a phising attack that replaces a host IP address with a bad one),
or if you use redirects without a syncRedirectDomain in the template.
<p/>
If your template is static, and you specify a syncRedirectDomain, signatures
aren't needed.
<p/>
Signatures are generated from a private key. The signature is based on the query string, properly URLEncoded, without the sig or key components.
<p>
The DNS Provider will verify the signature by fetching the public key from DNS.
This is gotten by doing a query for TXT records in DNS at the host name
specified in the query string as the key= value, in the domain specified by 
syncPubKeyDomain in the template.
<p/>
The format of the public key in DNS can be found in the spec at: <a href="https://github.com/Domain-Connect/spec/blob/master/Domain%20Connect%20Spec%20Draft.adoc#digitally-sign-requests">https://github.com/Domain-Connect/spec/blob/master/Domain%20Connect%20Spec%20Draft.adoc#digitally-sign-requests</a>
<p/>
<h1>Test Form</h1>
This form can test your signature generation.
<p/>
The public key will either fetch the public key from the DNS TXT Key/Domain,
or if specified will use the Public Key (the contents of the key minus the --BEGIN/END--- blocks).
<p/>
<form method="post" action="sig_verify">
<table>
<tr><td>DNS TXT Key:</td><td><input name="key" type="text"></td></tr>
<tr><td>Domain:</td><td><input name="domain" type="text"></td></tr>
<tr><td>Public Key:</td><td><input name="publickey" type="text"></td><br/></tr>
<tr><td>Sig:</td><td><input name="sig" type="text"></td></tr>
<tr><td>Query String:</td><td><input name="qs" type="text"></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Verify Signature" /></td></tr>
</table>
</form>

<h1>Public Key Generator</h1>

<script>
function generate()
{
	var text = document.getElementById("text").value;
	text = text.replace(/\s/g, "");
	var chunkSize = 200;
	
	var chunks = Math.ceil(text.length / chunkSize);
	
	var chunkId = 0;
	
	var result = "DNS TXT Records<p/>";
	
	for (var chunkId = 0; chunkId < chunks; chunkId++)
	{
		result = result + "<p style='white-space:nowrap'>";
		result = result + "p=" + String(chunkId + 1) + ",a=RS256,d=" + text.substring(chunkId * chunkSize, chunkId * chunkSize + chunkSize);
		result = result + "</p>";
	}
		       
	document.getElementById("output").innerHTML = result;
}
</script>
Paste the contents of the public key below. This is the base 64 content (not the -----BEGIN PUBLIC KEY----- or ----END PUBLIC KEY-----).
<p/>
Note: No data is sent to the server
<p/>
<textarea id=text rows=5 cols=80>
</textarea>
<p/>
<button name=Generate onclick="javascript:generate()">Generate</button>
<p/>
<span id=output>
</span>

% include('footer.tpl')

