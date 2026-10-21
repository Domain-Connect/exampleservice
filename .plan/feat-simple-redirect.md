# simple-redirect — iteration plan

**Branch:** feat/simple-redirect (from feat/dc-txt-override) **Started:** 2026-10-21 **Issue:** none yet (`gh` not logged in)
**Goal:** `/simple_post` applies template 1 in the same window with `redirect_uri` to `/simple_confirm`.
**Stash:** none

## Tasks

- [~] Requirement and failing tests
- [ ] `/simple_post` link with `redirect_uri`, `/simple_confirm`
- [ ] Gates, docs, restart the test service
- [ ] Issue and PR (based on feat/dc-txt-override) once `gh` is logged in
- [ ] Promote findings, delete this file

## Findings

- `views/simple_post.tpl` opens the apply URL with `window.open`, sized by the settings' `width`/`height`.
- template1 has `syncRedirectDomain: exampleservice.domainconnect.org` (Templates repository); `/sync_post` already builds an unsigned template 1 URL with `redirect_uri`.
- `gh auth status` fails in this container: no issue, no push.

## Decisions

- Branch stacked on feat/dc-txt-override: the test service runs both.
- Return page `/simple_confirm` (domain, sub-domain, link to the site); `error` renders `sync_error.tpl`.

## Corrections

## Open questions
