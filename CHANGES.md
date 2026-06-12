# Changes

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
