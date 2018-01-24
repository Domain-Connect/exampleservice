% include('header.tpl', title='Asynchronous Configuration')

<h1>Async Confirm</h1>
An status of '{{status_code}}' was returned applying the template.
<p/>
% if status_code == '200':
  You've applied '{{applied_template}}' to '{{domain}}' 
  % if subdomain != '' and subdomain != None:
      with sub domain '{{subdomain}}' 
  % end
  with the message '{{message}}'. You can apply Template 1 or Template 2 to any of the authorized domain/sub-domains.
% end

<h1>Interesting information (read only):</h1>
<table>
<tr><td>Domain:</td><td>{{domain}}</td></tr>
<tr><td>Hosts:</td><td>{{hosts}}</td></tr>
<tr><td>DNS Provider:</td><td>{{dns_provider}}</td></tr>
<tr><td>Access Token:</td><td>{{access_token}}</td></tr>
</table>
<form method="post" action="/async_confirm">
<h1>Apply template:</h1>
<input name=domain type=hidden value="{{domain}}"/>
<input name=hosts type=hidden value="{{hosts}}"/>
<input name=dns_provider type=hidden value="{{dns_provider}}"/>
<input name=access_token type=hidden value="{{access_token}}"/>
<table>
<tr><td>Domain:</td><td>{{domain}}</td></tr>
<tr><td>Hosts:</td><td>{{hosts}}</td></tr>
<tr><td>Sub Domain:</td><td><input size=50 name=subdomain type=text value=""/></td></tr>
<tr><td>Message:</td><td><input size=50 name=message type=text value=""/></td></tr>
<tr><td>Force:</td><td><input type="checkbox" name="force" value="1"/></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Apply Template 1"/></td>
<tr><td>&nbsp;</td><td><input type="submit" value="Apply Template 2" name="template2"/></td>
</table>
</form>
%include('footer.tpl')

