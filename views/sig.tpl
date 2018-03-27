% include('header.tpl', title='Signature Verification')

<h1>Signature Verification Test</h1>
<form method="post" action="sig_verify">
<table>
<tr><td>Domain:</td><td><input name="domain" type="text"></td></tr>
<tr><td>Key:</td><td><input name="key" type="text"></td></tr>
<tr><td>Sig:</td><td><input name="sig" type="text"></td></tr>
<tr><td>QS:</td><td><input name="qs" type="text"></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Verify Signature" /></td></tr>
</table>
</form>

% include('footer.tpl')

