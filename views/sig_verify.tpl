% include('header.tpl', title='Signature Verification')

<h1>Signature Verification Test</h1>

% if verified:
<h1 style="color:green">Passed</h1>
% else:
<h1 style="color:red">Failed</h1>
% end

<h3>Domain</h3>
{{domain}}

<h3>Key</h3>
{{key}}

<h3>Sig</h3>
{{sig}}

<h3>QS</h3>
{{qs}}

<h3>Public Key</h3>
{{pubKey}}

% include('footer.tpl')

