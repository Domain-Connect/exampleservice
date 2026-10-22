# simple-template2 — iteration plan

**Branch:** feat/simple-template2 (from feat/simple-redirect) **Started:** 2026-10-22 **Issue:** none yet (`gh` not logged in)
**Goal:** `/simple_post` checks and applies template 2 with a signature, keeping `redirect_uri` to `/simple_confirm`.
**Stash:** none

## Tasks

- [~] Requirement and failing tests
- [ ] `/simple_post`: template 2 check, signed apply URL
- [ ] Gates, docs, restart the test service
- [ ] Issue and PR (based on feat/simple-redirect) once `gh` is logged in
- [ ] Promote findings, delete this file

## Findings

- template2 (Templates repository): A `@` `%IP%`, TXT `@` `%RANDOMTEXT%` (prefix `shm:`), CNAME `whd` → `@`; `syncPubKeyDomain` and `syncRedirectDomain` `exampleservice.domainconnect.org`.
- `/sync_post` signs the query string with `redirect_uri` and appends `&sig=…&key=_dck1` (sync.py).

## Decisions

- Stacked on feat/simple-redirect: the test service runs all three branches.
- Same signing as `/sync_post`: `sigutil.generate_sig(config.priv_key, qs)` over the query string with `redirect_uri`.

## Corrections

## Open questions
