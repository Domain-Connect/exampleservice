% include('header.tpl', title='Configure Domain Connect')
<h1>Provider Found</h1>
Your domain uses {{providerName}}
<p/>
<a target=_new href='{{synchronousTargetUrl}}'>Configure Synchronously</a>
<p/>
<a target=_new href='{{synchronousSignedTargetUrl}}'>Configure Synchronously with Signature verification (not supported by all providers)</a> (Verified = {{verified}})
<p/>
% if asynchronousTargetUrl != None:
    <a href='{{asynchronousTargetUrl}}'>Configure Asynchronously</a>
% else:
    Async not supported by provider
% end
% include('footer.tpl')