
function domain_connect(domain, host, data, providerId, serviceId, cb) {

    // Query for the _domainconnect TXT record
    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'https://dns.google/resolve?type=txt&name=_domainconnect.' + domain);
    xhr.responseType = "json";
    xhr.onerror = function(e) {
	cb('', domain, host, '', data);
	return;
    };
    xhr.onload = function(e) {

	if (!this.response || this.status != 200 || this.response['Status'] != 0) {
	    cb('', domain, host, '', data);
	    return;
	}

	len = this.response['Answer'].length;
	if (len === 0) {
	    cb('', domain, host, '', data);
	    return;
	}

	// Get the value of the TXT record
	d = this.response['Answer'][len-1]['data'];
	d = d.split('"').join('');

	// Get the JSON for the settings
	xhr2 = new XMLHttpRequest();
	xhr2.open('GET', 'https://' + d + '/v2/' + domain + '/settings');
	xhr2.responseType = "json";
	xhr.onerror = function(e) {
	    cb('', domain, host, '', data);
	    return;
	};

	xhr2.onload = function(e) {
	    if (!this.response || this.status != 200) {
		cb('', domain, host, '', data);
	    }
	    
	    url_api = this.response['urlAPI'];
	    url_sync = this.response['urlSyncUX'];
	    dns_provider_name = this.response['providerName'];

	    // Verify our template is supported
	    xhr3 = new XMLHttpRequest()
	    xhr3.open('GET', url_api + '/v2/domainTemplates/providers/' + providerId + '/services/' + serviceId);
	    xhr3.onerror = function(e) {
		cb('', domain, host, '', data);
		return;
	    }
	    xhr3.onload = function(e) {
		if (!this.response || this.status != 200) {
		    cb('', domain, host, '', data);
		    return;
		}

		cb(url_sync + '/v2/domainTemplates/providers/' + providerId + '/services/' + serviceId + '/apply?domain=' + domain + '&host=' + host, domain, host, dns_provider_name, data);
		return;
	    }
	    xhr3.send();
	}
	xhr2.send();
    };
    xhr.send();
}
