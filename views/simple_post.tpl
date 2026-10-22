% include('header.tpl', title='DC Example Service')

<h2>Provider Found: Your domain uses {{providerName}}</h2>

Your provider is {{providerName}}. 
% if dc_txt:
<p>_domainconnect record: {{dc_txt}} (dc_txt)</p>
% end

<a href='{{synchronousSignedRedirectUrl2}}'>Click here for one easy setup.</a>
<p/>
{{providerName}} applies the template and sends you back here.

% include('footer.tpl')