% include('header.tpl', title='Asynchronous Configuration')

<h2>Access Granted</h2>
Access has been granted.
<p/>
<h4>Interesting information (read only):</h4>
<table border=1 cellpadding=3>
<tr><td>Domain:</td><td>{{domain}}</td></tr>
<tr><td>Hosts:</td><td>{{hosts}}</td></tr>
<tr><td>DNS Provider:</td><td>{{dns_provider}}</td></tr>
<tr>
	<td valign="top">oAuth&nbsp;Response&nbsp;Code&nbsp;from&nbsp;consent:</td>
	<td><div style="font-family:courier;word-break:break-all">{{code}}</div></td>
</tr>
<tr>
	<td valign="top">URL to fetch access token</td>
	<td><div style="font-family:courier;word-break:break-all">{{url}}</div></td>
</tr>
<tr>
	<td valign="top">JSON from Access Token Fetch</td>
	<td><pre id="json" style="font-family:courier"><pre></td>
</tr>
<tr>
	<td valign="top">Access Token:</td>
	<td><div style="font-family:courier;word-break:break-all">{{access_token}}</div></td>
</tr>
</table>

<script>document.getElementById("json").innerHTML = JSON.stringify({{!json_response}}, undefined, 2);</script>
<h2>Next Step</h2>
  <form method="post" action="/async_confirm">

  <input name=domain type=hidden value="{{domain}}"/>
  <input name=hosts type=hidden value="{{hosts}}"/>
  <input name=dns_provider type=hidden value="{{dns_provider}}"/>
  <input name=access_token type=hidden value="{{access_token}}"/>
  <table>
  <tr><td>Domain:</td><td>{{domain}}</td></tr>
  <tr><td>Hosts:</td><td>{{hosts}}</td></tr>
  <tr><td>---</td><td></td></tr>
  <tr><td>Message:</td><td><input size=50 name=message type=text value=""/></td></tr>
  <tr><td>---</td><td></td></tr>
  <tr><td>Sub Domain:</td><td><input size=50 name=subdomain type=text value=""/></td></tr>
  <tr><td>Force:</td><td><input type="checkbox" name="force" value="1"/></td></tr>
  <tr><td>&nbsp;</td><td><input type="submit" value="Apply Template 1"/></td>
  <tr><td>&nbsp;</td><td><input type="submit" value="Apply Template 2" name="template2"/></td>
  </table>
  </form>
% include('footer.tpl')

