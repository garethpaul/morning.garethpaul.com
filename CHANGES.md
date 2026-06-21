# Changes

## 2026-06-21

- Migrated the TomTom Calculate Route contract from the obsolete route service
  to `api.tomtom.com` and the `routes[0].summary.trafficDelayInSeconds` field.
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
