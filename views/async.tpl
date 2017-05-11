<html>

<body>
<h1>Access Granted</h1>
Access has been granted. Normally the server would later provision the template onto the domain.
<p/>
Here we simply emulate this asynchronous provisioning by allowing the template to be applied now.
<form method="post" action="/asyncconfig">
<table>
<tr><td>Domain:</td><td><input name=domain type=text readonly value="{{domain}}"/></td></tr>
<tr><td>Message:</td><td><input name=message type=text readonly value="{{message}}"/></td></tr>
<tr><td>API Url Root:</td><td><input name=urlAPI type=text readonly value="{{urlAPI}}"/></td></tr>
<tr><td>Access Token (oAuth):</td><td><input name=access_token type=text readonly value="{{access_token}}"/></td></tr>
<tr><td>&nbsp;</td><td><input type="submit"/></td>
</table>
</form>
</body>
</html>
