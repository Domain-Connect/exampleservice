<html>
<head>
<style>body {font-family: "Trebuchet MS", Helvetica, sans-serif;}</style>
</head>

<body>
<h1>Access Granted</h1>
Access has been granted. Normally the server would later provision the template onto the domain.
<p/>
Here we simply emulate this asynchronous provisioning by allowing the template to be applied now.
<form method="post" action="/asyncconfig">
<table>
<tr><td>Domain:</td><td><input size=50 name=domain type=text readonly value="{{domain}}"/></td></tr>
<tr><td>Message:</td><td><input size=50 name=message type=text readonly value="{{message}}"/></td></tr>
<tr><td>API Url Root:</td><td><input size=50 name=urlAPI type=text readonly value="{{urlAPI}}"/></td></tr>
<tr><td>Code:</td><td><input size=50 name=urlAPI type=text readonly value="{{code}}"/></td></tr>
<tr><td>JSON from Access Token Fetch</td><td><textarea name=json_response type=text readonly rows="10" cols="50">{{json_response}}</textarea></td></tr>
<tr><td>Access Token (oAuth):</td><td><input size=50 name=access_token type=text readonly value="{{access_token}}"/></td></tr>
<tr><td>&nbsp;</td><td><input type="submit"/></td>
</table>
</form>
</body>
</html>
