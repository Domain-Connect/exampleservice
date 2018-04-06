% include('ddns_header.tpl', title='Domain Connect Dynamic DNS')

<script>
  function copy(id) {
    let copyText = document.getElementById(id);
    copyText.select();
    document.execCommand("Copy");
    }
</script>

<h1>Access Granted</h1>
Access has been granted.
<br/><br/>
   
Please copy the following code and enter it into the installer.
<br/><br/>
<input type="text" id="code" value="{{oauth_code}}" readonly size="50" style="font-size: 25px"></input>

<button type="button" onclick="copy('code')" style="font-size: 25px">Copy to clipboard</button>

% include('ddn_footer.tpl')

