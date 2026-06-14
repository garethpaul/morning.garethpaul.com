# TomTom Parser Error Redaction

status: completed

## Summary

Prevent malformed TomTom response bodies from remaining reachable through a
chained `JSONDecodeError` after the parser raises its stable validation error.

## Problem Frame

`parse_delay_seconds` currently translates malformed JSON to a stable
`ValueError`, but exception chaining retains the complete provider body in the
decoder error's `doc` attribute. Error reporters or framework diagnostics can
therefore recover response content that the public message intentionally
omits.

## Requirements

- Preserve the existing stable malformed-JSON error message.
- Raise the validation error without a cause or exception context that retains
  the provider response body.
- Preserve successful parsing and all existing transport, size, and delay
  validation behavior.
- Add runtime and static regression coverage plus security documentation.

## Key Technical Decisions

- Record JSON decode failure inside the handler and raise the stable error only
  after leaving the handler, matching the existing transport-error redaction
  boundary.
- Keep the change local to malformed JSON; valid JSON shape and delay-value
  validation remain unchanged.

## Implementation Units

### U1: Prove and remove parser exception retention

**Files:** `stuff/tomtom.py`, `tests/test_tomtom.py`

**Approach:** Add a secret-bearing malformed payload regression test, then move
the stable parser error outside the decoder exception handler.

**Execution note:** Start with the failing regression test.

**Test scenarios:**

- A malformed response containing a private token raises the existing stable
  error with no cause, no context, and no token in the public message.
- Valid dictionary and JSON-string delay payloads continue to parse.

**Verification:** Focused parser tests pass and the regression fails when the
deferred error boundary is removed.

### U2: Protect and document the boundary

**Files:** `scripts/check-baseline.py`, `README.md`, `SECURITY.md`, `VISION.md`,
`CHANGES.md`, `docs/plans/2026-06-14-tomtom-parser-error-redaction.md`

**Approach:** Extend repository contracts and operator guidance so future
changes cannot silently restore decoder exception chaining.

**Test scenarios:**

- Static validation rejects removal of the deferred parser failure flag, the
  no-context assertions, documentation, or completed verification record.

**Verification:** All repository gates and targeted hostile mutations pass.

## Scope Boundaries

- Do not log, persist, or inspect live TomTom responses.
- Do not change endpoint routing, credentials, response-size limits, or delay
  semantics.

## Work Completed

- Moved malformed-JSON failure publication outside the decoder exception
  handler so the stable validation error has no retained cause or context.
- Added a secret-bearing regression test that proves the provider body is not
  reachable through the public parser exception.
- Extended the static baseline and maintained documentation with the parser
  error-redaction contract.

## Verification Completed

- `make lint`, `make test`, `make build`, and `make check` passed with nineteen
  offline tests and no live TomTom access.
- The focused parser regression passed after first failing against the retained
  `JSONDecodeError` cause.
- Seven hostile mutations covering the deferred source boundary, regression
  test, four documentation surfaces, and completed plan status were rejected.
