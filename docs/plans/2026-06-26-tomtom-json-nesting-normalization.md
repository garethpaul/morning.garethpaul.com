# TomTom JSON Nesting Normalization

status: completed

## Problem

The bounded response reader permits up to 1 MiB of decompressed content. A
much smaller JSON value with roughly 10,000 nested arrays reaches Python 3.12's
decoder recursion limit, causing `parse_delay_seconds` to expose raw
`RecursionError` instead of its stable malformed-JSON `ValueError`.

## Scope

- Normalize only `RecursionError` raised by `json.loads`.
- Preserve the body-free malformed-JSON message and empty exception context.
- Preserve response limits, route schema, accepted delay values, transport
  handling, and the dashboard's narrow degraded state.

## Work Completed

- Added a red-first Python 3.12 regression for a 20,001-byte nested payload.
- Included decoder recursion failure in the existing deferred invalid-JSON
  boundary.
- Extended static and documentation contracts for the new case.

## Verification Completed

- The focused regression failed with raw `RecursionError` before the fix and
  passed with the stable parser error afterward.
- Full `make check` passed in the reviewed Python 3.12 constraints environment.
- Isolated source and regression-test mutations were rejected by the baseline
  and runtime gates.

## Boundary

This change does not increase the response limit, add a custom JSON parser,
catch unrelated runtime failures, retain provider bodies, or make live calls.
