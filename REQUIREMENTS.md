# Requirements

What the example service has to do. The protocol is the
[Domain Connect specification](https://github.com/Domain-Connect/spec); the templates are
`exampleservice.domainconnect.org` `template1` and `template2` in
[Domain-Connect/Templates](https://github.com/Domain-Connect/Templates).

Requirements use MUST (required), SHOULD (expected, a gap has to be named) and MAY.

## Goals

1. **Demonstrate the protocol.** Each flow shows a developer the steps of Domain Connect: discovery,
   template check, the apply URL, signatures, OAuth. Diagnostic pages show the data of each step.
2. **Simple.** The hosted site is a message; the code stays short enough to read as an example.
3. **Stateless.** The service stores nothing: the hosted message lives in DNS.

## Hosts and configuration

- H1 MUST: `config.hosting_website` (`APP_DOMAIN`, default `exampleservice.domainconnect.org`)
  serves the service. Every route but `/` and `/static/` answers 404 for another host or for a
  protocol other than `config.protocol` (`APP_PROTOCOL`, default `https`).
- H2 MUST: `/` on `config.hosting_website` over `config.protocol` renders the home page with links
  to every flow, the signature tools and both templates. Over another protocol it redirects to
  `https://<hosting_website>` when `config.protocol` is `https`, and is 404 otherwise.
- H3 MUST: `config.ip` (`APP_IP`) is the address the templates' A record points to.
- H4 MUST: `/ddnscode` serves only `config.dynamicdns_website`.

## Hosted site

- S1 MUST: `/` on any other host reads that host's TXT records. Records of the form
  `shm:<seconds>:<text>` are the message, one line per record, ordered by `<seconds>`. A record
  `shm:<text>` counts as `<seconds>` 0.
- S2 MUST: a host with no such record is 404.
- S3 SHOULD: a host starting with `whd.` without a message shows the message of the host without
  that label (template 2 adds the `whd` CNAME).

## Input

- I1 MUST: a domain is 4 to 255 characters, labels of 1 to 63 letters, digits or `-`, not starting
  or ending with `-`; one trailing dot is allowed.
- I2 MUST: a message is 1 to 255 characters of `a-z A-Z 0-9 space , . ? !`.
- I3 MUST: invalid input renders `invalid_data.tpl`.
- I4 MUST: the TXT value written is `shm:<seconds since epoch>:<message>`.

## Discovery

- D1 MUST: discovery reads `_domainconnect.<domain>` TXT; exactly one record is required.
- D2 MUST: the settings are `GET https://<record>/v2/<domain>/settings`; a status other than 200
  fails discovery.
- D3 MUST: when the settings contain `nameServers`, the first authoritative NS of the domain is in
  that list; otherwise discovery fails.
- D4 MUST: a failure renders `no_domain_connect.tpl` with the reason (no record, no settings, no
  name servers, not authoritative, internal error).
- D5 MUST: support of each template the flow uses is checked with
  `GET <urlAPI>/v2/domainTemplates/providers/<provider>/services/<template>`; a status other than
  200 is *Missing template support*.
- D6 MUST: the popups of the sync flow are the settings' `width` and `height`, 750 × 750 when absent.
- D7 MUST: `dc_txt` in the query of `/simple_index`, `/sync_index`, `/async_index` and `/client`
  is used as the `_domainconnect` record of any domain entered; DNS is not queried for it and the
  `nameServers` check (D3) is skipped. The index page passes it on with the form.
- D8 MUST: `dc_txt` is a domain (I1) or IPv4 address, an optional port (1 to 65535) and an optional
  path of `a-z A-Z 0-9 . _ ~ / -`; otherwise
  the POST renders `invalid_data.tpl`.
- D9 MUST: the result pages show the `dc_txt` value in use.
- D10 MUST: `dc_proto` in the query of the same pages is the protocol of the settings call (D2),
  `http` or `https`; otherwise the POST renders `invalid_data.tpl`. The index page passes it on
  with the form; the sync and async result pages show the settings URL with it.

## Simple flow (`/simple_index`, `/simple_post`, `/simple_confirm`)

- F1 MUST: domain, optional sub-domain and message; discovery and the check of template 2; a link
  that opens the sync apply URL of template 2 in the same window, naming the DNS Provider. The
  query string is that of Y3 with `redirect_uri`
  `<protocol>://<hosting_website>/simple_confirm?domain=…&subdomain=…`, each value quoted, followed
  by `&sig=<signature of the query string>&key=_dck1`.
- F2 MUST: `/simple_confirm` shows the FQDN and a link to it, or `sync_error.tpl` when `error` is
  set.

## Synchronous flow (`/sync_index`, `/sync_post`, `/sync_confirm`)

- Y1 MUST: domain, optional sub-domain and message; discovery and the check of both templates.
- Y2 MUST: shows the `_domainconnect` record, the settings JSON, the template check URLs, the query
  string and four apply URLs: template 1, template 2 signed, and both again with `redirect_uri`.
- Y3 MUST: the query string is `domain`, `RANDOMTEXT`, `IP`, and `host` when a sub-domain is given,
  in this order, each quoted. Template 2 appends `&sig=<signature of the query string>&key=_dck1`;
  with a redirect, `redirect_uri` is part of the signed query string.
- Y4 MUST: `redirect_uri` is `<protocol>://<hosting_website>/sync_confirm?domain=…&subdomain=…`.
  `/sync_confirm` shows the domain and sub-domain, or `sync_error.tpl` when `error` is set.

## Asynchronous flow (`/async_index`, `/async_post`, `/async_oauth_response`, `/async_confirm`)

- A1 MUST: domain and hosts; discovery and the check of both templates.
- A2 MUST: only DNS Providers in `config.oAuthSecrets` and `config.oAuthAPIURLs` (keyed by
  `providerName`), whose `urlAPI` equals the configured URL, are accepted; otherwise
  *Not onboarded as oAuth provider*.
- A3 MUST: the consent URL is `<urlAsyncUX>/v2/domainTemplates/providers/<provider>` with `domain`,
  `host`, `client_id` (the provider id), `scope` (`template1+template2`) and `redirect_uri`
  (`/async_oauth_response` with `domain`, `hosts`, `dns_provider`).
- A4 MUST: `/async_oauth_response` exchanges `code` for an access token at
  `<oAuthAPIURL>/v2/oauth/access_token` (POST, `grant_type=authorization_code`, the same
  `redirect_uri`) and shows the code, the request and the token response. `error` set, or a status
  of 300 or more, renders `async_error.tpl` with the reason.
- A5 MUST: `/async_confirm` applies template 1, or template 2 when `template2` is posted, with
  `POST <oAuthAPIURL>/v2/domainTemplates/providers/<provider>/services/<template>/apply` and the
  bearer token, `force` 1 when ticked, and shows the URL and the status code.
- A6 MUST: the access token is not stored; the page posts it back.

## Signature tools (`/sig`, `/sig_generate`, `/sig_fetch`, `/sig_verify`, `/sig_verify_url`)

- G1 MUST: signatures are RS256 (PKCS#1 v1.5, SHA-256) over the query string, base64.
- G2 MUST: generate signs a query string with a pasted private key, or `config.priv_key` when none
  is given.
- G3 MUST: the public key of `<key>.<domain>` is the `d=` values of its TXT records joined in `p=`
  order; a record with `a=` other than `RS256` or `t=` other than `x509` rejects the key. Fetch
  shows the key and the records.
- G4 MUST: verify checks a signature against a pasted public key or the key from DNS; verify URL
  takes `sig` and `key` from an apply URL and verifies the rest of its query string.
- G5 MUST: `config.priv_key` matches the key published at `_dck1.exampleservice.domainconnect.org`.

## Client side (`/client`, `static/domainconnect.js`)

- C1 MUST: discovery runs in the browser (`dns.google` DNS-over-HTTPS, then the settings) and
  builds the sync apply URL of template 1; no signature, no server call.
- C2 MUST: a domain without Domain Connect is reported on the page.

## Dynamic DNS landing page (`/ddnscode`)

- N1 MUST: shows the OAuth `code` for the Dynamic DNS demo, or `ddns_error.tpl` when `error` is
  set.

## Running

- R1 MUST: runs under uWSGI behind nginx (`statelesshosting:app`), with Docker Compose for local
  use, and with Bottle's development server.
- R2 MUST: Python 3.14, packages `bottle`, `dnspython`, `cryptography`, `requests`.
