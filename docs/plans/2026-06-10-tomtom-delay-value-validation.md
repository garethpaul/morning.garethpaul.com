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

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- mutation checks for boolean and negative-value rejection
- `git diff --check`

## Work Completed

- Separated route-field lookup from delay value validation.
- Rejected booleans before Python can treat them as integers.
- Accepted only integer values or trimmed ASCII digit strings.
- Rejected fractional, signed-string, blank, and negative values with a stable
  error that does not include response content.
- Added offline boundary tests and mutation-sensitive baseline documentation.
