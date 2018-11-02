% include('header.tpl', title='Signature Verification')

<h1>Signature Verification Test</h1>
This form can be used to test the Service Providers signature generation.
<p/>
Singatures for synchronous templates are generated from the query string. The resulting value is typically appeneded to the querystring as sig=&lt;value&gt;.
<p/>
The corresponding public key for the signature is published inside DNS. The zone is specified in the template in syncPubKeyDomain. The values are specified in TXT records in this zone. The host of these records is also appended to the querystring as key=&lt;value&gt;.
<p/>
The format of the public key in DNS can be found in the spec at: <a href="https://github.com/Domain-Connect/spec/blob/master/Domain%20Connect%20Spec%20Draft.adoc#digitally-sign-requests">https://github.com/Domain-Connect/spec/blob/master/Domain%20Connect%20Spec%20Draft.adoc#digitally-sign-requests</a>
<p/>
Input a domain name, and key for the TXT record to get the public key. Or input the public key.
<form method="post" action="sig_verify">
<table>
<tr><td>Domain:</td><td><input name="domain" type="text"></td></tr>
<tr><td>DNS TXT Key:</td><td><input name="key" type="text"></td></tr>
<tr><td>Public Key (optional):</td><td><input name="publickey" type="text"></td></tr>
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
	var chunkSize = 200;
	
	var chunks = Math.ceil(text.length / chunkSize);
	
	var chunkId = 0;
	
	var result = "DNS TXT Records<p/>";
	
	for (var chunkId = 0; chunkId < chunks; chunkId++)
	{
		result = result + "p=" + String(chunkId + 1) + ",a=RS256,d=" + text.substring(chunkId * chunkSize, chunkId * chunkSize + chunkSize);
		result = result + "<p/>";
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

