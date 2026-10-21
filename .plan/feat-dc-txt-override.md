# dc-txt-override — iteration plan

**Branch:** feat/dc-txt-override **Started:** 2026-10-21 **Issue:** #23
**Goal:** `dc_txt` on the simple, sync, async and client flows replaces the `_domainconnect` TXT lookup for any domain; `dc_proto` sets the protocol of the settings call.
**Stash:** none

## Tasks

- [x] Investigate discovery and the flows
- [x] Requirements and failing tests
- [x] `util`: `dc_txt` in discovery, validation
- [x] Simple, sync, async: hidden field, POST, result page note
- [x] Client: `static/domainconnect.js` takes the override
- [x] Gates, docs
- [x] `dc_proto`: requirement, failing tests, code
- [x] Port in `dc_txt`
- [~] PR as draft, maintainer checks the pages
- [ ] File issue: `static/domainconnect.js` sets `xhr.onerror` for the settings request and does not return after a failed settings response
- [ ] Promote findings, delete this file

## Findings

- Discovery is `util.get_domainconnect_json(domain)`, called by `simple_post`, `sync_post`, `async_post` (simple.py:34, sync.py:31, async.py:29).
- The flows POST from the index pages; the parameter reaches the POST as a hidden field.
- `/client` runs discovery in `static/domainconnect.js` via `dns.google`; no `nameServers` check there.
- `.agent-sync.yml` of the merged `chore/python-3.14` was left over; removed after the maintainer confirmed no agent is active.

- 12 new tests failed before the code, 28 of 28 pass after.
- Dev server on 8082 (8081 is held by the maintainer's own server): 7 of 7 GET pages 200; `dc_txt=domainconnect.api.godaddy.com` with `example.com` finds GoDaddy in all three flows; `dc_txt=api.cloudflare.com/client/v4/dns/domainconnect` reaches the template check; `dc_txt=bad?x` is Invalid Data.
- CLAUDE.md, DEVELOPING.md, REQUIREMENTS.md, TESTING.md are in `.git/info/exclude`: their changes stay local.

- `dc_proto`: 10 new tests failed first, 38 of 38 pass. Live on 8082 with `dc_txt=domainconnect.api.godaddy.com`, `example.com`: `http` → *No json returned for /settings* (GoDaddy answers 404 over http), `https` → GoDaddy found, `ftp` → Invalid Data, in all three flows.
- Port: maintainer found `example.org:8443` and `172.17.0.6:5016` rejected as Invalid Data. After the fix, live on 8082 with `dc_proto=http`: `example.org:8443` → *No json returned for /settings* (fetched), `172.17.0.6:5016` → *Internal error* (not reachable from this container), `:0` and `:99999` → Invalid Data. 39 of 39 tests pass.

## Decisions

- Parameter name `dc_txt` (maintainer).
- All four flows (maintainer).
- With `dc_txt`, the `nameServers` check is skipped (maintainer).
- `dc_proto` is `http` or `https`, independent of `dc_txt`; it applies only to the settings call, the template check and apply URLs come from the settings.
- `dc_txt` is a host name or IPv4 address, an optional port 1 to 65535 and an optional path of `[A-Za-z0-9._~/-]`; otherwise `invalid_data.tpl`.

## Corrections

- `dc_txt` first rejected a port; ports are allowed now (maintainer).
- Notes about `dc_txt` on the index and client pages removed (maintainer); D9 covers result pages only.
- Playwright screenshots dropped (maintainer); rules updated in CLAUDE.md, DEVELOPING.md §3.7, TESTING.md §6.

## Open questions
