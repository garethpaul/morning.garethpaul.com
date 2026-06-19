# TomTom Delay Value Validation

status: completed

## Problem

The route parser currently passes the delay field through `int()`. Python then
accepts booleans and truncates fractional floats, while negative values can
reach the dashboard even though route delay is a non-negative integer.

## Scope

- Accept non-negative integer delay values.
- Preserve compatibility with ASCII digit strings returned by fixtures or the
  route service.
- Reject booleans, floats, signed strings, blanks, and negative integers.
- Return a stable validation error without including response content.
- Add offline unit and mutation coverage plus documentation guardrails.

## Work Completed

- Separated route-field lookup from delay value validation.
- Rejected booleans before Python can treat them as integers.
- Accepted only integer values or trimmed ASCII digit strings.
- Rejected fractional, signed-string, blank, and negative values with a stable
  error that does not include response content.
- Added offline boundary tests and mutation-sensitive baseline documentation.

## Verification Completed

- `make check`
- `make lint`
- `make test`
- `make build`
- `python3 -m py_compile scripts/check-baseline.py`
- `git diff --check`
- Canonical push Check run `27397385338` and pull-request Check run
  `27397386885` completed successfully at exact head
  `bffbd99b97eb8868ee9e618ecf4be2132ed33a64`.
- Hostile mutations confirmed the checker rejects an incomplete status,
  unfinished verification, altered run evidence, removed boolean rejection,
  and removed negative-value rejection.
- The implementation preserves `isinstance(value, bool)`,
  `normalized.isascii()`, and `if delay < 0`.
- `test_parse_delay_seconds_accepts_non_negative_integers` and
  `test_parse_delay_seconds_rejects_invalid_delay_values` cover the accepted
  and rejected value contracts.
