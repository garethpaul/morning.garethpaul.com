# TomTom Transport Error Redaction

status: completed

## Context

The legacy TomTom endpoint carries the API key in the request path. Requests
transport and HTTP status exceptions can include that full URL when Flask or a
process supervisor logs an uncaught error.

## Requirements

- Convert Requests transport and HTTP status failures to one stable error that
  does not include the request URL, API key, or chained exception.
- Preserve response closure for status, streaming, parsing, and success paths.
- Keep bounded streaming, timeout, HTTPS, and injected-client behavior intact.
- Add offline tests, mutation-sensitive static contracts, documentation, and
  completed verification evidence.

## Scope Boundaries

- Do not make live TomTom requests, add credentials, change endpoint routing,
  or alter successful delay parsing.

## Verification

- Run all Make gates, focused unit tests, Python compilation, hostile
  mutations, diff checks, artifact scans, and secret scans.

## Work Completed

- Converted Requests transport and HTTP status failures to a stable
  `TomTom request failed` error after leaving the exception handler.
- Preserved deterministic response closure and existing bounded parsing,
  timeout, HTTPS, and injected-client behavior.
- Added offline timeout and HTTP status tests proving the stable error has no
  cause, context, request URL, or API key.

## Verification Completed

- `make lint`, `make test`, `make build`, and `make check` passed with eighteen
  offline tests and no live TomTom access.
- Focused TomTom tests, Python compilation, repository constraint contracts,
  diff checks, artifact scans, and secret scans passed. A standalone
  `python -m pip check` reported the shared host's pre-existing
  `virtualenv 20.24.6` / `platformdirs 4.10.0` mismatch; hosted CI installs the
  repository's reviewed constraints in a clean environment.
- Six hostile mutations covering the Requests exception type, deferred error
  flag, transport test, context assertion, secret assertion, and completed
  plan evidence were rejected.
