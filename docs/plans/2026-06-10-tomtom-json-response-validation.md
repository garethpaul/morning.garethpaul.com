# TomTom JSON Response Validation

status: completed

## Context

`parse_delay_seconds` accepts fixture dictionaries and live TomTom response
text. Malformed response text should fail with a stable parser error before the
code attempts to read `route.summary.totalDelaySeconds`.

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
