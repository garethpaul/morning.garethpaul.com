# TomTom Transport Error Redaction

status: planned

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
