% include('header.tpl', title='Asynchronous Configuration')
% if applied == 0:
<h1>Access Granted</h1>
Access has been granted to {{domain}}.
<br/><br/>
% else:
<h1>Applied</h1>
You've applied a template to {{domain}} 
% if subdomain != '' and subdomain != None:
      with sub domain '{{subdomain}}'
% end
. You can apply either template to the same domain, or to another sub domain.
% end
<h1>Interesting information (read only):</h1>
<table>
% if applied == 0:
<tr><td>oAuth Response Code from consent:</td><td>{{code}}</td></tr>
<tr><td>JSON from Access Token Fetch</td><td>{{json_response}}</td></tr>
% end
<tr><td>Domain:</td><td>{{domain}}</td></tr>
<tr><td>API Url Root from DNS Provider:</td><td>{{urlAPI}}</td></tr>
<tr><td>Access Token:</td><td>{{access_token}}</td></tr>
</table>
<form method="post" action="/asyncconfig">
<h1>Apply template:</h1>
<input size=50 name=domain type=hidden value="{{domain}}"/>
<input size=50 name=urlAPI type=hidden value="{{urlAPI}}"/>
<input size=50 name=access_token type=hidden value="{{access_token}}"/>
<table>
<tr><td>Sub Domain:</td><td><input size=50 name=subdomain type=text value="{{subdomain}}"/></td></tr>
<tr><td>Message:</td><td><input size=50 name=message type=text value="{{message}}"/></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Apply Template 1"/></td>
<tr><td>&nbsp;</td><td><input type="submit" value="Apply Template 2" name="template2"/></td>
</table>
</form>
%include('footer.tpl')

