# simple-redirect — iteration plan

**Branch:** feat/simple-redirect (from feat/dc-txt-override) **Started:** 2026-10-21 **Issue:** #25
**Goal:** `/simple_post` applies template 1 in the same window with `redirect_uri` to `/simple_confirm`.
**Stash:** none

## Tasks

- [x] Requirement and failing tests
- [x] `/simple_post` link with `redirect_uri`, `/simple_confirm`
- [x] Gates, docs, restart the test service
- [~] Issue and PR (based on feat/dc-txt-override)
- [ ] Promote findings, delete this file

## Findings

- `views/simple_post.tpl` opens the apply URL with `window.open`, sized by the settings' `width`/`height`.
- template1 has `syncRedirectDomain: exampleservice.domainconnect.org` (Templates repository); `/sync_post` already builds an unsigned template 1 URL with `redirect_uri`.
- 3 new tests failed first, 43 of 43 pass. Test service (`exampleservice.internal:8081`, `APP_IP=172.25.0.2`): 8 of 8 GET pages 200; `/simple_post` with `dc_txt=domainconnect.api.godaddy.com` links to `https://dcc.godaddy.com/manage/v2/.../template1/apply?...&redirect_uri=http%3A%2F%2Fexampleservice.internal%3A8081%2Fsimple_confirm%3F...`.
- A real DNS Provider accepts the redirect only to `syncRedirectDomain` `exampleservice.domainconnect.org`.

## Decisions

- Branch stacked on feat/dc-txt-override: the test service runs both.
- Return page `/simple_confirm` (domain, sub-domain, link to the site); `error` renders `sync_error.tpl`.

## Corrections

- The redirect test lacked the NS record its settings' `nameServers` needs; added.

## Open questions
