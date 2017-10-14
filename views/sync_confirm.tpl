% include('header.tpl', title='Synchronous Configuration')

<h1>Applied</h1>
You've applied a template to domain '{{domain}}'
% if subdomain:
  and subdomain '{{subdomain}}'
% end

%include('footer.tpl')

