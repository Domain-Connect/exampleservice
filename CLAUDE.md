# CLAUDE.md

Guidance for Claude Code (claude.ai/code) in this repository.

## Project Overview

The Domain Connect example service: a Service Provider that demonstrates the Domain Connect protocol with "stateless hosting". A user enters a domain, optional sub-domain and a message; the service discovers the domain's DNS Provider and applies a template that sets an A record (the server's IP) and a TXT record (the message). A request for any other host renders the message read from that host's TXT records.

A Python 3 [Bottle](https://bottlepy.org/) application, server-side templates in `views/`, one browser script in `static/`. Published at `exampleservice.domainconnect.org`; upstream is [Domain-Connect/exampleservice](https://github.com/Domain-Connect/exampleservice) (remote `upstream`); work goes to the fork [pawel-kow/exampleservice](https://github.com/pawel-kow/exampleservice) (remote `origin`), PRs against its `master`, nothing pushed to `upstream`.

The behaviour is specified in [REQUIREMENTS.md](REQUIREMENTS.md); code conventions and process are in [DEVELOPING.md](DEVELOPING.md), checks in [TESTING.md](TESTING.md). Read them before you change a flow, and keep them current.

## Writing

All text (docs, comments, commits, PRs, issues, page text) is concise: facts in short words; rationale only when far from obvious; never alternatives or justification by contrast; current state only, no references to issues, requirement ids, dates or history. History is in git. Details: [DEVELOPING.md](DEVELOPING.md) §1.

## The external inputs

Details: [DEVELOPING.md](DEVELOPING.md) §3.10.

- The [Domain Connect specification](https://github.com/Domain-Connect/spec): discovery, settings keys, sync and async flows, signatures.
- The service templates `exampleservice.domainconnect.org` `template1` and `template2` in [Domain-Connect/Templates](https://github.com/Domain-Connect/Templates): the variables the code passes (`IP`, `RANDOMTEXT`, `host`) and which template needs a signature.
- Live DNS and DNS Provider endpoints: `_domainconnect` TXT records, settings responses, template support, OAuth.
- The public key in DNS at `_dck1.exampleservice.domainconnect.org`, matching `config.priv_key`.

Information none of them gives is a question for the maintainer, never a guess.

## Working on This Repository (agents)

Full rules: [DEVELOPING.md](DEVELOPING.md) §3.

1. **Branch mutex first** (§3.1): if `.agent-sync.yml` exists here, stop and poll every 15 minutes. Otherwise create it atomically with `timestamp`/`branch`/`issue`. Never commit it; remove it when finished and the checkout is back on `master`.
2. **Clean start** (§3.2): `master` must be clean. If not, **stop and ask the maintainer**: stop, or stash and pop at the end (a task in the plan). Then `git pull --ff-only origin master`.
3. **Branch** (§3.3): every iteration has its own branch from `master`.
4. **Plan** (§3.11): before changing anything, write `.plan/<branch>.md` (`/` → `-`; tasks, findings with evidence, decisions, corrections, open questions), commit and push it, keep it current, exactly one task `[~]`.
5. **Checks first** (§3.4): a requirement in REQUIREMENTS.md and a failing test in `tests/` before code.
6. **Pages** (§3.7): a change to a page or what it renders is checked by the maintainer in a browser against the dev server; no screenshots, no Playwright. The PR is marked ready only after acceptance.
7. **PR** (§3.6): one per iteration, a draft until the gates pass and the maintainer accepted it. Merging is done by hand.
8. **Before merge:** defects found but not fixed → GitHub issue (`bug` or `refactoring` plus a `severity: *` label); behavioural decisions → REQUIREMENTS.md; rationale → commit message. Then `git rm -r .plan` in its own commit.

Open defects and follow-up work are GitHub issues, not markdown. `gh` must be logged in (`gh auth login`); push with `git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push`.

## Layout

- `statelesshosting.py`: the WSGI app (`app`, `application`); route `/` (home page or hosted site) and `/static/<filename>`; imports the routes of every flow module with `from <module> import *`.
- Flow modules, one per area: `simple.py`, `sync.py`, `async.py`, `sig.py`, `client.py`, `ddns.py`. Each registers its routes on Bottle's default app with `@route`.
- `util.py`: discovery (`get_domainconnect_json`), template check, input validation, the message TXT format. `sigutil.py`: RS256 signatures and the public key read from DNS.
- `config.py`: server IP, host names and protocol (environment `APP_IP`, `APP_DOMAIN`, `APP_PROTOCOL`), provider and template ids, the sample private key, OAuth secrets and API URLs per DNS Provider.
- `views/`: Bottle SimpleTemplate pages, `<flow>_<step>.tpl`, framed by `header.tpl` and `footer.tpl`.
- `static/`: `domainconnect.js` (discovery in the browser via `dns.google`), the logo.
- `uwsgi.ini`, `uwsgi_params`, `nginx.conf`: production; [INSTALL.md](INSTALL.md) describes it.
- `docker-compose.yml`, `docker/`: local stack, nginx on port 8001 for `exampleservice.domainconnect.local`; [docker/README.md](docker/README.md).
- `tests/`: automated checks ([TESTING.md](TESTING.md)).
- `.scratchpad/`: scratch files, ignored by git (see Tools).
- `.plan/`: the plan of the current iteration, removed before merge.

## Development Commands

```bash
.venv/bin/pip install -r requirements.txt                       # dependencies (the dev container runs this on create)
.venv/bin/python -m compileall -q *.py                          # syntax of every module
.venv/bin/python -m pytest tests/                               # tests
APP_DOMAIN=localhost:8081 APP_PROTOCOL=http APP_IP=127.0.0.1 \
  .venv/bin/python -c "import bottle, statelesshosting; bottle.run(statelesshosting.app, host='127.0.0.1', port=8081)"
                                                                # dev server at http://localhost:8081/
curl -s -H 'Host: localhost:8081' http://127.0.0.1:8081/sig      # one page
docker compose up --build                                       # local stack at http://exampleservice.domainconnect.local:8001
```

All gates: [TESTING.md](TESTING.md) §5.

## Tools

- Available: `jq`, `curl`, `python3`, `gh`, `docker`. `dig` is not installed; resolve DNS with `.venv/bin/python -c "import dns.resolver; ..."` or `curl 'https://dns.google/resolve?type=TXT&name=_domainconnect.<domain>'`.
- Run Python only from the virtualenv at `.venv/` (ignored by git), never with the system interpreter or a system-wide `pip install`. Create it if it is missing with `python3 -m venv .venv`, install packages with `.venv/bin/pip install <pkg>`.
- Dependencies are listed in both `requirements.txt` (used by the dev container and Docker) and `Pipfile`; change both together.
- Keep scratch files in `.scratchpad/`, not in the session scratchpad the harness offers under `/tmp` and not elsewhere in this repository:
  - `.scratchpad/<YYYY-MM-DD>-<topic>/`: one folder per session or task, for intermediate files and downloads. Create a new one; reuse an existing one when you resume that task.
  - `.scratchpad/shared/`: large tools that stay the same between sessions. Reuse them; do not install them again per session.

## Rules for the code

- Every route except `/` and `/static/` serves only the host `config.hosting_website` over `config.protocol` and answers 404 otherwise; `/ddnscode` serves only `config.dynamicdns_website`. Local requests need a matching `Host` header and `APP_DOMAIN`/`APP_PROTOCOL`.
- `/` on any other host renders that host's message; it is the hosted site and takes no input but DNS.
- Request values and DNS data are third-party text: render them with `{{ }}` (escaped). `{{! }}` only for JSON the server serialised itself, and for `messagetext`, whose characters `is_valid_message` restricts.
- The private key and OAuth secrets in `config.py` are public sample values. Never add a real secret, key or token to the repository.
- Template ids, variable names and the signature key id `_dck1` match the published templates and DNS; change them only together with those.
- Match the style of the surrounding code ([DEVELOPING.md](DEVELOPING.md) §2).

## File Reference

- `README.md`, `INSTALL.md`: what the service is, production install
- `CLAUDE.md`, `DEVELOPING.md`, `TESTING.md`, `REQUIREMENTS.md`: agent guidance, conventions and process, checks, behaviour
- `.plan/<branch>.md`: plan of the current iteration
- `.devcontainer/`: dev container (Python 3.14, `gh`, Docker in Docker); creates `.venv/` from `requirements.txt`
- `.agent-sync.yml`: agent mutex, never committed
- `statelesshosting.py`, `simple.py`, `sync.py`, `async.py`, `sig.py`, `client.py`, `ddns.py`: routes
- `util.py`, `sigutil.py`, `config.py`: discovery and validation, signatures, configuration
- `views/`, `static/`: pages, browser script and logo
- `requirements.txt`, `Pipfile`, `Pipfile.lock`: dependencies
- `uwsgi.ini`, `uwsgi_params`, `nginx.conf`: production server; `docker-compose.yml`, `docker/`: local stack
