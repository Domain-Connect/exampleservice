% include('header.tpl', title='Asynchronous Configuration')

<h1>Applied</h1>
You've applied a template to {{domain}} 
% if subdomain != '' and subdomain != None:
    with sub domain '{{subdomain}}'
% end
. You can apply either template to the same domain, or to another sub domain.

<h1>Interesting information (read only):</h1>
<table>
<tr><td>Domain:</td><td>{{domain}}</td></tr>
<tr><td>API Url Root from DNS Provider:</td><td>{{urlAPI}}</td></tr>
<tr><td>Access Token:</td><td>{{access_token}}</td></tr>
</table>
<form method="post" action="/async_confirm">
<h1>Apply template:</h1>
<input name=domain type=hidden value="{{domain}}"/>
<input name=hosts type=hidden value="{{hosts}}"/>
<input name=urlAPI type=hidden value="{{urlAPI}}"/>
<input name=access_token type=hidden value="{{access_token}}"/>
<table>
<tr><td>Sub Domain:</td><td><input size=50 name=subdomain type=text value="{{subdomain}}"/></td></tr>
<tr><td>Message:</td><td><input size=50 name=message type=text value="{{message}}"/></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Apply Template 1"/></td>
<tr><td>&nbsp;</td><td><input type="submit" value="Apply Template 2" name="template2"/></td>
</table>
</form>
%include('footer.tpl')

