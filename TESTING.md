# Testing

Test layers, conventions and gates.

Related: [DEVELOPING.md](DEVELOPING.md) §3.4 (when tests are written),
[REQUIREMENTS.md](REQUIREMENTS.md) (what the tests hold the service to).

Tests pin the requirements, not the markup.

---

## 1. Principles

### 1.1 Substitute the network, not the code

| Seam              | Substituted with                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------ |
| **DNS**           | `dns.resolver.resolve` replaced in the test (`monkeypatch`) with canned answers             |
| **HTTP**          | `requests.get` / `requests.post` replaced with canned responses; the requested URL is checked |
| **Host, protocol** | the WSGI environ (`HTTP_HOST`, `wsgi.url_scheme`) of the request                          |
| **Configuration** | `APP_DOMAIN`, `APP_PROTOCOL`, `APP_IP` in the environment before `config` is imported       |
| **Keys**          | `config.priv_key` and a public key derived from it in the test                              |

Never patch a function of this repository to make a test pass. Automated tests never reach live
DNS or a DNS Provider.

### 1.2 Behaviour, not structure

Assert on what a request returns and what the service sends: status, redirect target, text on the
page, the URLs built (query string order, quoting, `sig`, `key`), the request made to the DNS
Provider. Not on markup or which helper was called.

---

## 2. Layers

| Layer   | Where                     | Runner                       | Real                             | Substituted                  |
| ------- | ------------------------- | ---------------------------- | -------------------------------- | ---------------------------- |
| Unit    | `tests/test_<module>.py`  | pytest (`.venv/`)            | `util`, `sigutil`, cryptography  | DNS, HTTP                    |
| Routes  | `tests/test_<flow>.py`    | pytest, WSGI calls to `statelesshosting.app` | routes, templates | DNS, HTTP, host, configuration |
| Live    | by hand                   | dev server, browser, `curl`  | DNS, DNS Providers               | nothing                      |

---

## 3. Tests (`tests/`)

Each test file covers one module or flow. A new behaviour gets its test in the file of its area, or
a new file listed here.

| File                | Pins |
| ------------------- | ---- |
| `test_util.py`      | Domain and message validation (I1, I2); TXT value format (I4); message parsing, order, legacy `shm:<text>`, no record (S1, S2); discovery: record count, settings status, name server check, each failure reason (D1–D4); template check (D5); `dc_txt` validation and discovery with it, settings over `dc_proto` (D7, D8, D10) |
| `test_sigutil.py`   | Sign and verify round trip with `config.priv_key`; a changed query string fails; public key assembly in `p=` order, rejection of other `a=` and `t=` (G1, G3) |
| `test_site.py`      | `/` on the hosting website, redirect to https, 404 for an unsupported protocol (H2); hosted site message and 404 (S1–S3); host gate of every route (H1, H4) |
| `test_simple.py`    | Invalid input, no Domain Connect, missing template; `dc_txt` and `dc_proto` passed on, used, rejected; the signed template 2 apply URL with `redirect_uri`, `/simple_confirm` and its error (I3, D4–D10, F1, F2) |
| `test_sync.py`      | Query string order and quoting, signature over it, `redirect_uri`, the four URLs, `/sync_confirm` and its error; `dc_txt`, `dc_proto` (D7–D10, Y1–Y4) |
| `test_async.py`     | Onboarding check, consent URL, code exchange request and errors, apply request with bearer token and `force`; `dc_txt`, `dc_proto` (D7–D10, A1–A6) |
| `test_sig.py`       | Generate with a pasted and the configured key, fetch, verify, verify URL (G2–G4) |

## 4. Live checks

| Check            | How |
| ---------------- | --- |
| Docker           | `docker compose up --build`, then `http://exampleservice.domainconnect.local:8001/` |
| Client `dc_txt`, `dc_proto` | `/client?dc_txt=<record>&dc_proto=http` in a browser builds the apply URL from that record, settings over http (D7, D10) |

## 5. Gates

| Gate                 | Command                                          | Where                 |
| -------------------- | ------------------------------------------------ | --------------------- |
| Syntax               | `.venv/bin/python -m compileall -q *.py`         | by hand               |
| App imports          | `.venv/bin/python -c "import statelesshosting"`  | by hand               |
| Tests                | `.venv/bin/python -m pytest tests/`              | by hand               |
| Pages render         | every GET route returns 200 from the dev server with the configured `Host` | by hand |
| Docker builds        | `docker compose build`                           | by hand, for dependency or Docker changes |
| No `.plan/` files    | `git ls-files .plan` is empty                    | by hand, before the PR is ready |

There is no CI; every gate is run before a change goes to review.

## 6. Tooling

- pytest in `.venv/` (`.venv/bin/pip install pytest`), a development dependency: not in
  `requirements.txt`.
- No screenshots or Playwright; pages are checked by the maintainer (DEVELOPING.md §3.7).

## 7. Coverage

| Area                                       | Expectation                                         |
| ------------------------------------------ | --------------------------------------------------- |
| [REQUIREMENTS.md](REQUIREMENTS.md)         | Every MUST and SHOULD pinned by a test in §3 or a live check in §4 |
| Bug fixes                                  | A test that reproduces the defect                    |
