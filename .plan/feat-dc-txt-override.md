# dc-txt-override — iteration plan

**Branch:** feat/dc-txt-override **Started:** 2026-10-21 **Issue:** #23
**Goal:** a `dc_txt` query parameter on the simple, sync, async and client flows replaces the `_domainconnect` TXT lookup for any domain.
**Stash:** none

## Tasks

- [x] Investigate discovery and the flows
- [~] Requirements and failing tests
- [ ] `util`: `dc_txt` in discovery, validation
- [ ] Simple, sync, async: hidden field, POST, result page note
- [ ] Client: `static/domainconnect.js` takes the override
- [ ] Gates, screenshots, docs
- [ ] PR as draft, maintainer acceptance
- [ ] Promote findings, delete this file

## Findings

- Discovery is `util.get_domainconnect_json(domain)`, called by `simple_post`, `sync_post`, `async_post` (simple.py:34, sync.py:31, async.py:29).
- The flows POST from the index pages; the parameter reaches the POST as a hidden field.
- `/client` runs discovery in `static/domainconnect.js` via `dns.google`; no `nameServers` check there.
- `.agent-sync.yml` of the merged `chore/python-3.14` was left over; removed after the maintainer confirmed no agent is active.

## Decisions

- Parameter name `dc_txt` (maintainer).
- All four flows (maintainer).
- With `dc_txt`, the `nameServers` check is skipped (maintainer).
- `dc_txt` is a host name with an optional path of `[A-Za-z0-9._~/-]`; otherwise `invalid_data.tpl`.

## Corrections

## Open questions
