% include('header.tpl', title='Asynchronous Configuration')

<h2>Async Confirm</h2>
A call to apply the template was made to:
<p/>
<div style="font-family:courier;word-break:no-break">{{url}}</div>
<p/>
A status of '{{status_code}}' was returned.
<p/>
% if status_code == '200':
  You've applied '{{applied_template}}' to '{{domain}}' 
  % if subdomain != '' and subdomain != None:
      with sub domain '{{subdomain}}' 
  % end
  with the message '{{message}}'. You can apply Template 1 or Template 2 to any of the authorized domain/sub-domains.
% end

<h2>Interesting information (read only):</h2>
<table border=1 cellpadding=3>
<tr><td>Domain:</td><td>{{domain}}</td></tr>
<tr><td>Hosts:</td><td>{{hosts}}</td></tr>
<tr><td>DNS Provider:</td><td>{{dns_provider}}</td></tr>
<tr><td valign="top">Access&nbsp;Token:</td><td><div style="font-family:courier;word-break:no-break">{{access_token}}</td></tr>
</table>
<form method="post" action="/async_confirm">

<h2>Apply template:</h2>
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

