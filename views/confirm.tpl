<html>

<body>
<h1>Provider Found</h1>
Your domain uses {{providerName}}
<p/>
<a target=_new href='{{synchronousTargetUrl}}'>Configure Synchronously</a>
<p/>
% if asynchronousTargetUrl != None:
    <a href='{{asynchronousTargetUrl}}'>Configure Asynchronously</a>
% else:
    Async not supported by provider
% end
</body>
</html>
