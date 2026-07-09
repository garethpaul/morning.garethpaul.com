# Changes

## 2026-07-09 - P2 - Add agent guidance and CODEOWNERS

### Summary

Added repository agent instructions and default CODEOWNERS so contributors and
automation have a durable ownership and workflow surface on `master`.

### Work completed

- Added `AGENTS.md` with make gates, constraints install, and secret-safe settings notes.
- Added `.github/CODEOWNERS` assigning the repository to `@garethpaul`.
- Extended the static baseline to require both files and keep a single hosted workflow.

### Files changed

- `AGENTS.md` — contributor and coding-agent guidance.
- `.github/CODEOWNERS` — default ownership.
- `scripts/check-baseline.py` — required-file and content contracts.
- `README.md` — repository contents listing.
- `CHANGES.md` — this cycle record.

### Validation

- `make check` — baseline, offline tests, and compile.

## 2026-06-26 12:20 - P1 - Normalize excessive TomTom JSON nesting

### Summary

Mapped Python's JSON decoder recursion limit to the dashboard's stable,
body-free malformed-response contract for bounded but excessively nested
TomTom payloads.

### Work completed

- Added a Python 3.12 regression using a 20,001-byte, 10,000-level JSON array.
- Normalized `RecursionError` beside decoder `ValueError` without broadening
  route, schema, delay, transport, or dashboard exception handling.
- Extended the static baseline, maintained documentation, and implementation
  record so the decoder boundary remains mutation-sensitive.

### Threads

- Started: TomTom JSON nesting normalization — direct implementation.
- Continued: continuous open-source maintenance loop.
- Stopped: none.

### Files changed

- `stuff/tomtom.py` — stable decoder recursion normalization.
- `tests/test_tomtom.py` — excessive-nesting redaction regression.
- `scripts/check-baseline.py` — source, test, documentation, and plan contracts.
- `README.md`, `SECURITY.md`, `VISION.md` — parser boundary guidance.
- `docs/plans/2026-06-26-tomtom-json-nesting-normalization.md` — completed plan.
- `CHANGES.md` — this cycle record.

### Validation

- Red Python 3.12 test — previously raised raw `RecursionError` from
  `json.loads`; now raises the stable context-free `ValueError`.
- Reviewed Python 3.12 `make check` — baseline, 37 offline tests, and source
  compilation passed.
- `pip check` — all 12 reviewed packages are compatible.
- Two isolated hostile mutations — removing the recursion catch or reducing
  the regression below the decoder limit both failed closed.
- `git diff --check` — passed.
- Hosted baseline runs `28259927059` and `28259924403` passed.
- CodeQL run `28259925258` passed actions and Python analysis; the aggregate
  CodeQL check also passed.
- `codex review --base origin/master` was attempted on exact head `9fbfeb3` but
  OpenAI authentication returned HTTP 401 before analysis; immutable manual
  diff review found no accepted or actionable findings.

### Bugs / findings

- P1: A response well below the 1 MiB bound could exceed the JSON decoder's
  nesting limit and escape the public parser's stable malformed-response type.

### Blockers

- None. The regression is offline and requires no TomTom key or live request.

### Next action

- Run the reviewed Python 3.12 gate, prove the new source/test contracts reject
  hostile mutations, and require exact-head hosted checks before merge.

## 2026-06-25 23:48 - P1 - Keep the dashboard usable during TomTom failures

### Summary

Converted the documented TomTom transport and parser failure surface into a
redacted traffic-unavailable state instead of replacing the whole dashboard
with a Flask 500 page.

### Work completed

- Added one shared route helper that catches only `RuntimeError` and `ValueError`.
- Preserved successful delay rendering, work/home routing, fuel-cost content,
  news content, and unexpected programming-error visibility.
- Added an explicit traffic-unavailable template state without rendering or
  logging provider exception details.
- Added a mutation-sensitive static contract and completed implementation plan.

### Threads

- Started: TomTom degraded dashboard — direct implementation.
- Continued: continuous open-source maintenance loop.
- Stopped: none.

### Files changed

- `app.py` — narrow provider-failure display helper shared by both routes.
- `templates/index.html` — explicit available/unavailable traffic states.
- `tests/test_app.py` — work/home outage, redaction, local-content, and
  unexpected-error regressions.
- `scripts/check-baseline.py` — durable degraded-dashboard contract.
- `README.md`, `SECURITY.md`, `VISION.md` — operational and security boundary.
- `docs/plans/2026-06-25-tomtom-degraded-dashboard.md` — completed plan.
- `CHANGES.md` — this cycle record.

### Validation

- Red Python 3.12 tests — `RuntimeError` and `ValueError` each returned 500
  before the helper was added; unexpected `TypeError` already propagated.
- Reviewed constraints environment — 36 offline tests passed.
- `/usr/bin/make check` — baseline, 36 tests, and source compilation passed.
- `uv pip check` — all 12 reviewed packages are compatible.
- Six isolated hostile mutations — all rejected across catch width, work/home
  coverage, unavailable copy, provider-detail retention, and unexpected-error tests.
- `git diff --check` — passed.
- Hosted and CodeQL gates pending.

### Bugs / findings

- P1: Stable provider transport, cleanup, response-bound, encoding, JSON,
  schema, and delay errors made otherwise local dashboard content unavailable.

### Blockers

- None. No live TomTom key, coordinates, response, or request is required.

### Next action

- Run the full reviewed Python 3.12 gate and hostile mutations, then require
  exact-head hosted checks and CodeQL before review and merge.

## 2026-06-25

- Added TomTom integer conversion redaction so oversized JSON integers and
  digit strings use stable validation errors without retained Python exceptions.

## 2026-06-21

- Migrated the TomTom Calculate Route contract from the obsolete route service
  to `api.tomtom.com` and the `routes[0].summary.trafficDelayInSeconds` field.
- Removed the retired TomTom key from the current checker while preserving
  digest-based reintroduction detection.
- Added offline rejection coverage for the legacy response shape and missing or
  malformed routes, summaries, and delay fields.
- Clarified that the repository name is historical, no deployment configuration
  is included, and live use requires local coordinates plus `TOMTOM_API_KEY`.
- Preserved the complete checkout root for absolute Makefile paths containing
  spaces, brackets, or apostrophes, and rejected `MAKEFILE_LIST` overrides.
- Added offline regression coverage for all eight Make aliases and command-line
  or environment root override attempts.

## 2026-06-19

- Rejected noncanonical coordinate tokens that Python accepts as numbers but
  TomTom route paths do not accept as decimal coordinates.
- Extended TomTom transport error redaction to response cleanup failures so a
  close exception cannot expose an API-key-bearing request URL.

## 2026-06-17

- Added coordinate whitespace normalization so validated commute coordinates
  produce canonical TomTom route paths without encoded component-edge spaces.

## 2026-06-16

- Added settings import error preservation so a missing dependency inside an
  existing local settings module is no longer misreported as absent configuration.
- Added finite positive commute settings validation so `NaN` and infinity fail
  during configuration loading and direct fuel-cost calculation.

## 2026-06-15

- Added TomTom invalid encoding redaction so invalid UTF-8 provider bytes use
  the same stable body-free parser error as malformed JSON.

## 2026-06-14

- Added TomTom parser error redaction so malformed provider response bodies are
  not retained through chained JSON decoder exceptions.

## 2026-06-13

- Made tests, compilation, static checks, verification, and generated-file
  cleanup resolve from the checkout for absolute Makefile invocations.
- Added TomTom transport error redaction so timeout and HTTP status failures do
  not retain the API-key-bearing request URL.

## 2026-06-10

- Added a reviewed 12-package Python 3.12 `constraints.txt` graph for hosted
  dependency resolution, explicit credential-free checkout, and exact
  workflow, cache, documentation, and plan contracts. Version constraints do
  not authenticate downloaded package artifacts.
- Upgraded the Flask compatibility range to `>=3.1.3,<3.2`, the patched line
  for `CVE-2026-27205` / `GHSA-68rp-wp8r-4726`.
- Added a bounded TomTom response reader that streams at most 1 MiB into JSON
  parsing and closes HTTP responses on success and failure.
- Added TomTom delay value validation so booleans, fractional values, and
  negative delays fail before dashboard rendering.
- Added pinned, read-only Python 3.12 hosted validation for dependency
  installation, `pip check`, and offline Flask/TomTom tests.
- Added TomTom JSON response validation so malformed route-service responses
  raise stable parser errors before delay parsing.

## 2026-06-09

- Updated check target gate order so `make check` delegates through `make lint`,
  `make test`, and `make build`.
- Added `make lint`, `make test`, and `make build` gate aliases alongside the
  existing `make check` baseline.
- Added TomTom API key placeholder validation so copied template keys fail
  before live route requests.
- Added coordinate setting validation so malformed home/work positions fail
  without echoing raw local values.
- Added coordinate range validation so impossible home/work positions fail
  without echoing raw local values.
- Added sanitized numeric setting errors so invalid commute configuration fails
  without echoing raw local values.
- Added repository-relative Flask assets so static and template files resolve
  correctly when the app is created outside the repository working directory.

## 2026-06-08

- Added `make check` with Python compilation and static baseline checks.
- Added offline tests for settings loading, Flask route rendering, TomTom URL construction, response parsing, and injected HTTP calls.
- Added `requirements.txt` for Flask and requests.
- Made commute-cost calculation load from explicit environment or ignored local settings.
- Added positive numeric commute settings validation for distance, fuel economy, and fuel cost.
- Moved committed settings placeholders to `settings.py.example` while allowing local `settings.py` at runtime.
- Fixed the `/home` route to request home traffic instead of the misspelled route key.
- Disabled Flask debug mode by default and allowed opt-in via `FLASK_DEBUG=1`.
- Kept TomTom route calls on HTTPS and removed the remote jQuery dependency.
