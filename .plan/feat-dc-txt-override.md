# dc-txt-override — iteration plan

**Branch:** feat/dc-txt-override **Started:** 2026-10-21 **Issue:** #23
**Goal:** a `dc_txt` query parameter on the simple, sync, async and client flows replaces the `_domainconnect` TXT lookup for any domain.
**Stash:** none

## Tasks

- [x] Investigate discovery and the flows
- [x] Requirements and failing tests
- [x] `util`: `dc_txt` in discovery, validation
- [x] Simple, sync, async: hidden field, POST, result page note
- [x] Client: `static/domainconnect.js` takes the override
- [x] Gates, docs
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

## Decisions

- Parameter name `dc_txt` (maintainer).
- All four flows (maintainer).
- With `dc_txt`, the `nameServers` check is skipped (maintainer).
- `dc_txt` is a host name with an optional path of `[A-Za-z0-9._~/-]`; otherwise `invalid_data.tpl`.

## Corrections

- Notes about `dc_txt` on the index and client pages removed (maintainer); D9 covers result pages only.
- Playwright screenshots dropped (maintainer); rules updated in CLAUDE.md, DEVELOPING.md §3.7, TESTING.md §6.

## Open questions
