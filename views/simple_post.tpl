% include('header.tpl', title='DC Example Service')

<h2>Provider Found: Your domain uses {{providerName}}</h2>

Your provider is {{providerName}}. 

<h3>Step 1</h3>
<a target=_new href='javascript:null(void);' onclick='window.open("{{synchronousUrl1}}", "", "width={{width}},height={{height}}");'>Click here for one easy setup.</a>

<h3>Step 2</h3>
<a href='http://{{fqdn}}'>Visit your site</a>

<p/>
Note: It may take a few minutes for your configuration to take affect.

% include('footer.tpl')