% include('header.tpl', title='Signature Verification')

<h1>Signatures</h1>
Signatures are sometimes needed with the synchronous protocol. This is necessary if your template
has variables that could be replaced by malicious values by a bad actor in a phising attack,
or if you are using redirects without a syncRedirectDomain in the template DNS Providers.
<p/>
If your template is mostly static and you aren't doing redirects, or if your 
template is mostly static and you are doing redirects but you specify a
syncRedirectDomain in your template then you don't need to sign your requests.
<p/>
The signature is generated from the properly URL Encoded query string. The Service Provider would 
generate a signature using a private key, appending the signature as sig=<value> onto the query string when
calling the DNS Provider.
<p/>
The DNS Provider will verify the signature by fetching the public key from DNS. This is fetched as a
series of TXT records from the dmain specified in syncPubKeyDomain in the template. The host name for these
records is added onto the query string as key=<value>.
<p/>
The format of the public key in DNS can be found in the spec at: <a href="https://github.com/Domain-Connect/spec/blob/master/Domain%20Connect%20Spec%20Draft.adoc#digitally-sign-requests">https://github.com/Domain-Connect/spec/blob/master/Domain%20Connect%20Spec%20Draft.adoc#digitally-sign-requests</a>
<p/>

<h1>Generating they Key Pair</h1>
To generate a key pair run the following commands:
<p/>
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
<p/>
openssl rsa -pubout -in private_key.pem -out public_key.pem
<p/>
You use the private key to generate your signature, and you publish the public key in DNS
for the DNS Provider to verify your signature.

<h1>Generating the Signature</h1>
This form will generate a signature. It allows a Service Provider to verify their code is 
generating the signature correctly.
<p/>
<font color="red">Warning:</font> This form does take the private key as a parameter. Normally your private key 
would be kept secret and not shared. As such it is not recommended that you use your production private key in this form. 
<p/>
The private key should be all the characters between the -----BEGIN/END----- block.
If the private key is not provided, the private key for the example service will be used.
<p/>
<form method="post" action="sig_generate">
<table>
<tr><td>Query String:</td><td><input name="qs" type="text"</td></tr>
<tr><td>Private Key:</td><td><input name="privatekey" type="text"></td><br/></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Generate Signature" /></td></tr>
</table>
</form>
<p>

<h1>Verifying the Signature from a Public Key</h1>
This form can test signature verification. You provide your query string, signature, and the public key. The public key should be all
the characters between the -----BEGIN/END----- block.
<p/>
<form method="post" action="sig_verify">
<table>
<tr><td>Sig:</td><td><input name="sig" type="text"></td></tr>
<tr><td>Query String:</td><td><input name="qs" type="text"></td></tr>
<tr><td>Public Key:</td><td><input name="publickey" type="text"></td><br/></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Verify Signature" /></td></tr>
</table>
</form>

<h1>Verifying the Signature from a Public Key in DNS</h1>
This form can test signature verification. You provide your query string and signature. Instead of providing the
public key, you provide the Host (normally passed as key=&lt;value&gt; on the query string) and the Domain (normally the syncPubKeyDomain in the template).

<p/>
<form method="post" action="sig_verify">
<table>
<tr><td>Sig:</td><td><input name="sig" type="text"></td></tr>
<tr><td>Query String:</td><td><input name="qs" type="text"></td></tr>
<tr><td>Host (key=<value>):</td><td><input name="key" type="text"></td></tr>
<tr><td>Domain (syncPubKeyDomain):</td><td><input name="domain" type="text"></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Verify Signature" /></td></tr>
</table>
</form>

<h1>Publishing the Public Key in DNS</h1>

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
This form will generate the DNS Records for publishing a public key. Paste the contents of the public key below. 
This is the base 64 content (not the -----BEGIN PUBLIC KEY----- or ----END PUBLIC KEY-----).
<p/>
<textarea id=text rows=5 cols=80>
</textarea>
<p/>
<button name=Generate onclick="javascript:generate()">Generate</button>
<p/>
<span id=output>
</span>

<h1>Fetching the Public Key from DNS</h1>
This form will allow you to test fetching your public key from DNS. You provide the Host (normally the key=&lt;value&gt; from the query string)
and the Domain (normally syncPubKeyDomain from the template).
<p/>
<form method="post" action="sig_fetch">
<table>
<tr><td>Host (key=<value>):</td><td><input name="key" type="text"></td></tr>
<tr><td>Domain (syncPubKeyDomain):</td><td><input name="domain" type="text"></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Fetch Key" /></td></tr>
</table>
</form>

% include('footer.tpl')

