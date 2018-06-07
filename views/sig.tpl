% include('header.tpl', title='Signature Verification')

<h1>Signature Verification Test</h1>
This form can be used to test the Service Providers signature generation.
<p/>
Singatures for synchronous templates are generated from the query string. The resulting value is typically appeneded to the querystring as sig=&lt;value&gt;.
<p/>
The corresponding public key for the signature is published inside DNS. The zone is specified in the template in syncPubKeyDomain. The values are specified in TXT records in this zone. The host of these records is also appended to the querystring as key=&lt;value&gt;.
<p/>
The format of the public key in DNS can be found in the spec at: <a href="https://github.com/Domain-Connect/spec/blob/master/Domain%20Connect%20Spec%20Draft.adoc#digitally-sign-requests">https://github.com/Domain-Connect/spec/blob/master/Domain%20Connect%20Spec%20Draft.adoc#digitally-sign-requests</a>
<p/
<form method="post" action="sig_verify">
<table>
<tr><td>Domain:</td><td><input name="domain" type="text"></td></tr>
<tr><td>Key:</td><td><input name="key" type="text"></td></tr>
<tr><td>Sig:</td><td><input name="sig" type="text"></td></tr>
<tr><td>Query String:</td><td><input name="qs" type="text"></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Verify Signature" /></td></tr>
</table>
</form>

% include('footer.tpl')

