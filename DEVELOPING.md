# Developing

Code, writing and process conventions for the example service.

Related: [REQUIREMENTS.md](REQUIREMENTS.md), [TESTING.md](TESTING.md), [CLAUDE.md](CLAUDE.md).

---

## 1. Writing

Applies to all text: docs, code comments, commit messages, PR descriptions, issues, page text.

- **Concise.** State facts in short words.
- **No rationale** unless it is far from obvious and needed to understand the fact.
- **No alternatives.** Never describe options not taken or justify by contrast to them.
- **Current state only.** No references to issues, requirement ids, dates or history in docs and
  comments. History is in git: commit messages and PR descriptions; issues are referenced from
  commits and PRs only. Requirement ids are defined in [REQUIREMENTS.md](REQUIREMENTS.md) and not
  cited elsewhere.

Page text is written for a developer learning Domain Connect: it names the protocol step a page
shows.

---

## 2. Code conventions

### 2.1 Style

| Code                    | Language and style                                                                                  |
| ----------------------- | --------------------------------------------------------------------------------------------------- |
| `*.py`                  | Python 3, Bottle; 4-space indent, single quotes; handlers registered with `@route` on the default app |
| `views/*.tpl`           | Bottle SimpleTemplate; `% include('header.tpl', title=...)` first, `% include('footer.tpl')` last   |
| `static/domainconnect.js` | Browser script, no build step, no dependencies                                                    |
| `tests/*.py`            | pytest, one file per module under test (TESTING.md §3)                                              |
| `docker/`, `*.ini`, `nginx.conf` | Match the existing files                                                                   |

No formatter is configured: match the surrounding code. Reformatting goes in a separate commit.

### 2.2 Naming

| Kind            | Convention                                          | Example                                  |
| --------------- | --------------------------------------------------- | ---------------------------------------- |
| Flow module     | the flow, one word                                  | `sync.py`, `sig.py`                      |
| Route           | `/<flow>_<step>`                                    | `/sync_post`, `/async_oauth_response`    |
| Handler         | the route without `/`                               | `sync_post`                              |
| View            | `<flow>_<step>.tpl`                                 | `sync_confirm.tpl`                       |
| Helper          | `snake_case`, verb phrase; `is_` for a predicate    | `get_domainconnect_json`, `is_valid_hostname` |
| Config value    | `snake_case` or the existing `camelCase` in `config.py` | `hosting_website`, `oAuthSecrets`    |
| Template id     | as published in the Templates repository            | `template1`, `template2`                 |

### 2.3 Comments

Only where the code is not self-explanatory:

- the protocol step a block implements (discovery, template check, apply URL, signature, OAuth
  code exchange);
- what the specification or a DNS Provider requires that the code cannot show;
- code that looks wrong but is right;
- what a broad `except` is for.

No commented-out code, changelog comments, or comments restating the code.

### 2.4 Error handling

- **A page, never a stack trace.** Invalid input renders `invalid_data.tpl`; a domain without
  usable Domain Connect renders `no_domain_connect.tpl` with the reason; an error returned by the
  DNS Provider renders the flow's `*_error.tpl`.
- **Never swallow errors.** A broad `except` returns a value the caller turns into a page with a
  reason.
- A host or protocol that the route does not serve is `abort(404)`.

### 2.5 Third-party content

Request parameters, DNS records, settings responses and OAuth responses are third-party text.

- Templates render them with `{{ }}`. `{{! }}` only for JSON the server serialised and for
  `messagetext`, which `is_valid_message` restricts to `[a-zA-Z ,.?!0-9]`.
- Values put into URLs are quoted with `urllib.parse.quote(value, '')`.
- `static/domainconnect.js` builds markup from DNS data: escape it before inserting HTML.
- No `print` or debug output left in the code.

---

## 3. Process

### 3.1 Agent branch mutex

`.agent-sync.yml` in the root of this repository marks the checkout as in use by an agent session.

1. Before any other action, check for it. If present: stop, poll every 15 minutes until gone.
   Its content is irrelevant.
2. Create it atomically (`set -o noclobber; { > .agent-sync.yml; } 2>/dev/null`). If creation
   fails, go back to 1.
3. Content:
   ```yaml
   timestamp: 2026-10-04T14:03:00Z
   branch: feat/<topic>
   issue: <GH issue number(s)>
   ```
4. Never commit it (it is in `.gitignore`).
5. Remove it when the iteration is finished and the checkout is back on `master`. A leftover file
   from a crashed session is removed by hand after confirming no agent is active.

### 3.2 Starting work

1. Check that `master` is clean (`git status --porcelain`). If not: **stop and ask the
   maintainer** whether to stop, or to stash and go on. A stash
   (`git stash push -u -m "<branch>: start"`) is recorded in the plan with a task to pop it on
   `master` at the end of the iteration (§3.11).
2. Bring `master` up to date: `git switch master && git pull --ff-only origin master`.
3. Create the branch (§3.3).

### 3.3 Branches

```
master                    no direct commits
  feat/<topic>            new flow, page or capability
  fix/<topic>             defect
  refactor/<topic>        behaviour-preserving restructuring
  docs/<topic>            documentation only
  chore/<topic>           tooling, dev container, Docker, dependencies
```

Branch from `master`, rebase to stay current. One concern per branch.

### 3.4 Test-driven development

Red → green → refactor. Mandatory for:

- behaviour: the requirement in [REQUIREMENTS.md](REQUIREMENTS.md) first, then a failing test in
  `tests/` (TESTING.md §3), then the code;
- every bug fix: a test reproducing the observed behaviour first.

Page layout and text: checked and accepted by the maintainer (§3.7).

### 3.5 Commits

```
<type>(<scope>): <imperative summary>

<what changed, if the summary doesn't say it; why, only if not obvious>

Refs: #<issue>
```

Types: `feat` `fix` `refactor` `test` `docs` `chore`. Scopes: `site`, `simple`, `sync`, `async`,
`sig`, `client`, `ddns`, `util`, `config`, `views`, `deps`, `docker`, `tests`, `dev`. Atomic,
revertable commits.

### 3.6 Review

- Every change goes through a PR against `master` of the fork
  [pawel-kow/exampleservice](https://github.com/pawel-kow/exampleservice) (`origin`). No branches
  or PRs on [Domain-Connect/exampleservice](https://github.com/Domain-Connect/exampleservice)
  (`upstream`).
- `gh` is used only to open issues and PRs, edit PR descriptions, and flip draft ⟷ ready. Merging,
  closing, commenting, triggering workflows and settings are done by hand in the GitHub UI.
- PR descriptions: intent and main changes; the pages checked (§3.7).
- The service is deployed by hand ([INSTALL.md](INSTALL.md)); there are no releases.

**Tier 1** (merge when the gates are green): docs, tests, page text and styling, dev tooling.

**Tier 2** (self-review, re-read the diff the next day, then merge): the protocol (discovery,
template check, apply URLs, signatures, OAuth); input validation; rendering of third-party text;
`config.py`; dependencies; Docker, uWSGI and nginx. **AI-assisted changes are always Tier 2**, and
the PR says so.

Tier 2 checklist, in the PR's diff view:

- [ ] Tests written first and failed first
- [ ] Every gate of TESTING.md §5 green
- [ ] No debug output, no commented-out code
- [ ] Third-party text escaped, URL values quoted, no real secret added
- [ ] [REQUIREMENTS.md](REQUIREMENTS.md) still accurate
- [ ] Pages checked in a browser and accepted (§3.7)
- [ ] Agentic work: plan findings promoted, `.plan/` removed (§3.11)

### 3.7 Pages before review

Applies to changes to `views/`, `static/`, or what a page renders.

1. Push the branch and open the PR as a draft.
2. Run the dev server (CLAUDE.md, Development Commands) and every gate (TESTING.md §5).
3. Give the maintainer the URLs and inputs of every affected state on the dev server and wait for
   acceptance. Agents take no screenshots and do not use Playwright. Change and repeat until
   accepted.
4. When clean and accepted: `gh pr ready`, and add what was checked to the PR description
   (`gh pr edit --body`).

### 3.8 GitHub issues

1. A defect or follow-up not yet on GitHub gets an issue before work starts.
2. An issue being worked on is moved to "In Progress".
3. The PR says `Closes #NN`.

Labels: `bug`, `refactoring`, `enhancement`, `documentation`; bugs also get a severity:
`severity: correctness bug` (🔴 a broken flow, a wrong DNS change, unescaped third-party text),
`severity: operational hazard or significant gap` (🟠), `severity: quality/maintainability` (🟡),
`severity: known/accepted` (🔵). An issue stands alone: quote code inline, name paths and lines,
state the fix.

Open defects and follow-up work are issues, not markdown.

### 3.9 Docs in the same iteration

Before opening the PR:

| Change                                              | Update                                                                   |
| --------------------------------------------------- | ------------------------------------------------------------------------ |
| Behaviour of a flow or page                         | [REQUIREMENTS.md](REQUIREMENTS.md)                                       |
| Code layout, conventions or pitfalls                | §2                                                                       |
| Tests added or changed                              | [TESTING.md](TESTING.md) §3                                              |
| New file, folder, route or command                  | [CLAUDE.md](CLAUDE.md) Layout, File Reference or Development Commands    |
| Dependencies                                        | `requirements.txt` and `Pipfile` together; [README.md](README.md) Dependencies |
| Dev container, Docker, setup                        | [README.md](README.md), [docker/README.md](docker/README.md), [CLAUDE.md](CLAUDE.md) |
| Production setup                                    | [INSTALL.md](INSTALL.md)                                                 |
| Template ids, variables or signature key            | `config.py`, the Templates repository, the `_dck1` DNS record            |
| Defect found but not fixed, or follow-up work       | GitHub issue (§3.8)                                                      |

When code and docs disagree, fix both.

### 3.10 External inputs

1. **Domain Connect specification**: discovery, settings keys, the sync and async flows,
   signatures. Behaviour that diverges from it is recorded in REQUIREMENTS.md.
2. **Templates repository**: `exampleservice.domainconnect.org.template1.json` and
   `.template2.json` define the records and variables; template 2 needs a signature.
3. **Live DNS and DNS Provider endpoints**: used by the flows at run time and for manual checks;
   never relied on by automated tests (TESTING.md §1.1).
4. **The `_dck1` public key in DNS**: must match `config.priv_key`.

Missing information is a question for the maintainer; never a guess.

### 3.11 Agentic workflows

Agents follow every rule above and keep a plan file per iteration.

1. Write `.plan/<branch>.md` (`/` in the branch name becomes `-`) after investigating, before the
   first edit.
2. Commit and push it, first commit on the branch, and again on material changes.
3. Task list with state: `[ ]` pending, `[x]` done, `[~]` in progress (exactly one).
4. Record findings with evidence as they are established ("6 of 6 GET pages return 200", not
   "works").
5. Keep it updated during the iteration.
6. Record course corrections, including own errors.
7. A stash taken at the start (§3.2) is a task: pop it on `master` after the merge.
8. Before merge, promote what is worth keeping, then `git rm -r .plan` in its own commit.

| Content                                 | Promote to                         |
| --------------------------------------- | ---------------------------------- |
| Defect not fixed, follow-up work        | GitHub issue (§3.8)                |
| Behavioural decision or constraint      | [REQUIREMENTS.md](REQUIREMENTS.md) |
| Why the change looks like it does       | Commit message, PR description     |
| Something surprising about the code     | Code comment where it surprises, or §2 |
| Something surprising about a DNS Provider | REQUIREMENTS.md, next to the behaviour it affects |

On ambiguity: record it under "Open questions" and ask the maintainer.

Template:

```markdown
# <topic> — iteration plan

**Branch:** feat/<topic> **Started:** YYYY-MM-DD **Issue:** #NN
**Goal:** <one sentence: what "done" means>
**Stash:** <none, or `stash@{n}` "<message>">

## Tasks

- [x] Investigate how X works
- [~] Add failing test for Y
- [ ] Implement Y
- [ ] Gates, page check, docs
- [ ] Promote findings, delete this file
- [ ] Pop the stash on `master` (only with a stash)

## Findings

- <fact> — <evidence: file:line, command output, measurement>

## Decisions

- <choice>

## Corrections

- <what was wrong, what changed>

## Open questions

- <needs a human answer>
```

---

## 4. Tooling

### 4.1 CI

There is no CI. The gates are run by hand (TESTING.md §5).

### 4.2 Dependencies

- Python packages in `requirements.txt` and `Pipfile`, changed together. The dev container and
  `docker/Dockerfile-web` install `requirements.txt`.
- The Python version of the dev container, `docker/Dockerfile-web`, `uwsgi.ini` (`plugin`) and
  `Pipfile` (`python_version`) is changed together.
- Dev tools: Python in `.venv/` only; other tools in `.scratchpad/shared/` at exact versions.

### 4.3 Git

`origin` is the fork `pawel-kow/exampleservice`, `upstream` is `Domain-Connect/exampleservice`;
both HTTPS, `gh repo set-default` is the fork. Push with `gh` credentials (`gh auth login` first):
`git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push`.
