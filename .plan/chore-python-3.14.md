# python-3.14 — iteration plan

**Branch:** chore/python-3.14 **Started:** 2026-10-21 **Issue:** none
**Goal:** the service installs, imports, passes its tests and runs in Docker on Python 3.14.
**Stash:** none

## Tasks

- [x] Investigate what fails on 3.14
- [x] Requirement R2 and failing tests for the site, util and sigutil
- [x] Load the async flow without `from async import *`
- [x] Upgrade bottle, cryptography, dnspython in `requirements.txt`, `Pipfile`, `Pipfile.lock`
- [x] `dns.resolver.resolve`, raw regex string
- [x] Python 3.14 in `docker/Dockerfile-web`, `uwsgi.ini`, `Pipfile`, INSTALL.md
- [x] Gates (TESTING.md §5), Docker build and live check
- [~] Push, draft PR (needs `gh auth login`)
- [ ] Issues for the defects below
- [ ] Promote findings, delete this file

## Findings

- `.venv` (3.14.8) is empty: `pip install -r requirements.txt` fails building cryptography 2.6.1 (`No module named 'pkg_resources'`).
- `statelesshosting.py:11` `from async import *` is a SyntaxError since Python 3.7 (`async` is a keyword); compileall fails.
- bottle 0.12 imports `cgi`, removed in Python 3.13; bottle 0.13.4 does not.
- `util.py:20` `"\d"` in a non-raw string: SyntaxWarning on compile.
- dnspython 2.9.0 keeps `dns.resolver.query`, deprecated; `resolve` is its replacement.
- `tests/` does not exist; TESTING.md §3 lists files that are not written.
- Red: before the code change, 4 of 11 util/sigutil tests fail on the `dns.resolver.query` DeprecationWarning and `tests/test_site.py` fails to import (SyntaxError). After: 17 of 17 pass.
- Gates: compileall clean (no SyntaxWarning), `import statelesshosting` ok, pytest 17 passed, `.plan` is the only tracked plan file.
- Dev server: `/`, `/simple_index`, `/sync_index`, `/async_index`, `/sig`, `/client` return 200. `/sync_post` for `domainconnect.org` discovers GoDaddy and builds both apply URLs with `sig=…&key=_dck1`.
- Docker: `docker compose build` ok; image runs Python 3.14.8, uWSGI 2.0.31; the same 6 pages return 200 through nginx on 8001; `/sig_fetch` reads `_dck1.exampleservice.domainconnect.org`.
- A signature from `config.priv_key` verifies against the live `_dck1` key (G5).
- Defect, not fixed: `/sync_index` and `/async_index` (and the other sync/async routes) do not check the host and protocol; H1 requires 404 — `sync.py:10`, `async.py:9`.
- Defect, not fixed: `/` on a host whose TXT records hold no `shm:` record renders 200 with no message; S2 requires 404 — `util.get_messagetext` returns `''`, `statelesshosting.py` checks only `None`. Seen live: `Host: example.com` → 200.
- Defect, not fixed: `statelesshosting.py` uses `request.header['Host']` in the `whd.` branch (S3); `request.header` does not exist.
- Installed in `.venv`: bottle 0.13.4, cryptography 50.0.2, dnspython 2.9.0, requests 2.34.2, pytest 9.1.1.

## Decisions

- Keep the file name `async.py` and load it with `importlib.import_module('async')`.
- Only the tests needed to pin this upgrade (site, util, sigutil); the rest of TESTING.md §3 is follow-up work.

## Corrections

## Open questions

- Production uWSGI plugin name for Python 3.14 (`uwsgi.ini` `plugin = python314`) depends on the host's packages.
- `gh` is not logged in: push and PR wait for `gh auth login`.
