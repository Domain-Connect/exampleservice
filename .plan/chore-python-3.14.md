# python-3.14 — iteration plan

**Branch:** chore/python-3.14 **Started:** 2026-10-21 **Issue:** none
**Goal:** the service installs, imports, passes its tests and runs in Docker on Python 3.14.
**Stash:** none

## Tasks

- [x] Investigate what fails on 3.14
- [~] Requirement R2 and failing tests for the site, util and sigutil
- [ ] Load the async flow without `from async import *`
- [ ] Upgrade bottle, cryptography, dnspython in `requirements.txt`, `Pipfile`, `Pipfile.lock`
- [ ] `dns.resolver.resolve`, raw regex string
- [ ] Python 3.14 in `docker/Dockerfile-web`, `uwsgi.ini`, `Pipfile`, INSTALL.md
- [ ] Gates (TESTING.md §5), Docker build and live check
- [ ] Push, draft PR (needs `gh auth login`)
- [ ] Promote findings, delete this file

## Findings

- `.venv` (3.14.8) is empty: `pip install -r requirements.txt` fails building cryptography 2.6.1 (`No module named 'pkg_resources'`).
- `statelesshosting.py:11` `from async import *` is a SyntaxError since Python 3.7 (`async` is a keyword); compileall fails.
- bottle 0.12 imports `cgi`, removed in Python 3.13; bottle 0.13.4 does not.
- `util.py:20` `"\d"` in a non-raw string: SyntaxWarning on compile.
- dnspython 2.9.0 keeps `dns.resolver.query`, deprecated; `resolve` is its replacement.
- `tests/` does not exist; TESTING.md §3 lists files that are not written.
- Installed in `.venv`: bottle 0.13.4, cryptography 50.0.2, dnspython 2.9.0, requests 2.34.2, pytest 9.1.1.

## Decisions

- Keep the file name `async.py` and load it with `importlib.import_module('async')`.
- Only the tests needed to pin this upgrade (site, util, sigutil); the rest of TESTING.md §3 is follow-up work.

## Corrections

## Open questions

- Production uWSGI plugin name for Python 3.14 (`uwsgi.ini` `plugin = python314`) depends on the host's packages.
- `gh` is not logged in: push and PR wait for `gh auth login`.
