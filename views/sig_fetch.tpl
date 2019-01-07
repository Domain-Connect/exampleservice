% include('header.tpl', title='Signature Public Key Fetch')

<h1>Signature Public Key Fetch</h1>

<h3>Domain</h3>
{{domain}}

<h3>Key</h3>
{{key}}

<h3>Public Key DNS Records</h3>
% if record_strings:
% for record in record_strings:
{{record}}
% end
<p/>
%end

<h3>Public Key</h3>
{{pubKey}}

% include('footer.tpl')

