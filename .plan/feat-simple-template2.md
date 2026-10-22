# simple-template2 — iteration plan

**Branch:** feat/simple-template2 (from feat/simple-redirect) **Started:** 2026-10-22 **Issue:** none yet (`gh` not logged in)
**Goal:** `/simple_post` checks and applies template 2 with a signature, keeping `redirect_uri` to `/simple_confirm`.
**Stash:** none

## Tasks

- [x] Requirement and failing tests
- [x] `/simple_post`: template 2 check, signed apply URL
- [x] Gates, docs, restart the test service
- [~] Issue and PR (based on feat/simple-redirect) once `gh` is logged in
- [ ] Promote findings, delete this file

## Findings

- template2 (Templates repository): A `@` `%IP%`, TXT `@` `%RANDOMTEXT%` (prefix `shm:`), CNAME `whd` → `@`; `syncPubKeyDomain` and `syncRedirectDomain` `exampleservice.domainconnect.org`.
- `/sync_post` signs the query string with `redirect_uri` and appends `&sig=…&key=_dck1` (sync.py).
- 3 tests failed first, 44 of 44 pass. Test service (`exampleservice.internal:8081`, `APP_IP=172.25.0.2`): 7 of 7 GET pages 200; `/simple_post` with `dc_txt=domainconnect.api.godaddy.com` links to `.../template2/apply?...&redirect_uri=...&sig=...&key=_dck1`; `/sig_verify_url` with that URL against `_dck1.exampleservice.domainconnect.org` in DNS: Passed.

## Decisions

- Stacked on feat/simple-redirect: the test service runs all three branches.
- Same signing as `/sync_post`: `sigutil.generate_sig(config.priv_key, qs)` over the query string with `redirect_uri`.

## Corrections

## Open questions
