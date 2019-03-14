% include('header.tpl', title='DC Example Service')

<h2>About Domain Connect</h2>
Domain Connect is an open standard that makes it easy for a user to configure DNS for a domain running at a DNS provider to work with a Service running at an independent Service Provider. The user can do so without understanding any of the complexities of DNS.
<h2>Example Service</h2>
Our service is a simple website builder. The website is designed, and then published on a specific domain with optional sub-domain.
<p/>
Our site builder is hands down the lamest possible. The site built consists of a simple message string. But to attach the domain and optional sub-domain, our site builder shines as an excellent Service Provider using the Domain Connect protocol.
<h2>Running the Service</h2>
There are several different versions of designing the site and attaching it to a domain an and optional sub-domain.
<p/>
<a href='/simple_index'>Simple Flow</a> shows a typical user interaction with Domain Connect. Use this if you want to experience a typical user experience.
<p/>
<a href='/sync_index'>Synchronous Flow Details</a> shows all the details of the protocol and how it works. It injects extra steps and diagnostic information and is intended for the developer.
<p>
<a href='/async_index'>Asynchronous Flow</a> shows all the details of the OAuth asynchronous version protocol. Like the Synchronous Flow Details, it injects extra steps and diagnostic information and is intended for the developer.
<h2>Tools</h2>
<a href='/sig'>Signature Tools</a> are available to aid the developer in generating valid signatures for use with certain templates.
<h2>Templates</h2>
The application uses two templates. Both are similar, but one adds an additional CNAME and ues signatures
<p>
<a target=_template1 href="https://github.com/Domain-Connect/Templates/blob/master/exampleservice.domainconnect.org.template1.json">Template 1</a>
<p/>
<a target=_template2 href="https://github.com/Domain-Connect/Templates/blob/master/exampleservice.domainconnect.org.template2.json">Template 2</a>
<p>

% include('footer.tpl')

