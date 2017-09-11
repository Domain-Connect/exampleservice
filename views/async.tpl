%include('header.tpl')

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
<form method="post" action="/asyncconfig">
<table>
% if applied == 0:
<tr><td>oAuth Response Code from consent:</td><td><input size=50 name=oAuthCode type=text readonly value="{{code}}"/></td></tr>
<tr><td>JSON from Access Token Fetch</td><td><textarea name=json_response type=text readonly rows="10" cols="50">{{json_response}}</textarea></td></tr>
% end
<tr><td>Domain:</td><td><input size=50 name=domain type=text readonly value="{{domain}}"/></td></tr>
<tr><td>API Url Root from DNS Provider:</td><td><input size=50 name=urlAPI type=text readonly value="{{urlAPI}}"/></td></tr>
<tr><td>Access Token:</td><td><input size=50 name=access_token type=text readonly value="{{access_token}}"/></td></tr>
</table>
<h1>Apply template:</h1>
<table>
<tr><td>Sub Domain:</td><td><input size=50 name=subdomain type=text value="{{subdomain}}"/></td></tr>
<tr><td>Message:</td><td><input size=50 name=message type=text value="{{message}}"/></td></tr>
<tr><td>&nbsp;</td><td><input type="submit" value="Apply Template 1"/></td>
<tr><td>&nbsp;</td><td><input type="submit" value="Apply Template 2" name="template2"/></td>
</table>
</form>
%include('footer.tpl')
