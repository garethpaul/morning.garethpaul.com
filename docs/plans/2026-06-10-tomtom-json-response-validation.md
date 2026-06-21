# TomTom JSON Response Validation

status: completed

## Context

At the time of this change, `parse_delay_seconds` accepted fixture dictionaries
and live TomTom response text using the then-current
`route.summary.totalDelaySeconds` field. Malformed response text needed to fail
with a stable parser error before field access. The provider contract was later
superseded by `docs/plans/2026-06-21-tomtom-calculate-route.md`.

## Completed Scope

- Caught malformed JSON response text before route delay parsing.
- Returned a stable `TomTom response must be valid JSON` error.
- Added offline unit coverage for malformed response text.
- Extended the static baseline and docs so TomTom JSON response validation
  remains visible.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
