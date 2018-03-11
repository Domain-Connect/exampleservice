<html>

<head>
<title>Domain Connect Example</title>
<style>body {font-family: "Trebuchet MS", Helvetica, sans-serif;}</style>
<script>
  function copy(id) {
    let copyText = document.getElementById(id);
    copyText.select();
    document.execCommand("Copy");
    }
</script>
</head>

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-102550640-1', 'auto');
  ga('send', 'pageview');
</script>

<body>
<a href="http://domainconnect.org"><img src="static/dclogo.png"></a>
<br/>

<h1>Access Granted</h1>
Access has been granted to {{domain}}.
<br/><br/>
   
Please copy the following code and enter it into the installer.
<br/><br/>
<input type="text" id="code" value="{{oauth_code}}" readonly size="50" style="font-size: 25px"></input>

<button type="button" onclick="copy('code')" style="font-size: 25px">Copy to clipboard</button>

</body>
</html>