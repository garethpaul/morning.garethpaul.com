# TomTom Delay Sanity Ceiling

status: completed

## Context

`parse_delay_seconds` accepted any non-negative integer, so a malformed or
hostile TomTom response could report an implausible advisory delay (for example
`99999999999`) and have it rendered as-is on the dashboard.

This branch was originally opened to fix an overflow `ValueError` for 5000-digit
values, but that premise did not hold. Merged plan
`2026-06-25-tomtom-integer-conversion-redaction.md` already maps both 5000-digit
forms to stable errors: an oversized JSON integer trips Python's
`int_max_str_digits` ceiling and maps to the malformed-JSON error, and an
oversized digit string raises inside the existing conversion handler. The base
branch test suite passes unmodified on the supported interpreter, and the
originally cited Python 3.8 behavior does not apply — `README.md` declares
Python 3.10+ and CI pins 3.12, while the 4300-digit limit was backported to
3.9.14 and 3.10.7.

What remains is therefore not an overflow fix but a semantic sanity ceiling for
plausible-length yet implausible values, which the base branch accepts.

## Requirements

- Reject `trafficDelayInSeconds` above a documented one-year ceiling, using the
  existing stable delay-value error so no provider data reaches the message.
- Apply the ceiling once, after type dispatch, alongside the existing negative
  check rather than duplicating it per branch.
- Name the ceiling as a module constant, matching
  `MAXIMUM_TOMTOM_RESPONSE_BYTES` and `TOMTOM_RESPONSE_CHUNK_BYTES`.
- Preserve the redaction contract asserted for oversized JSON integers; the
  ceiling must not relax any existing assertion.
- Cover the boundary explicitly: at the ceiling accepts, above it rejects.

## Work Completed

- Hoisted the ceiling to `MAXIMUM_TOMTOM_DELAY_SECONDS = 365 * 24 * 60 * 60`,
  documenting that TomTom publishes no upper bound and that the value is a
  plausibility ceiling rather than a provider limit.
- Applied the ceiling once after type dispatch, next to the existing
  `delay < 0` check, and removed the per-branch duplicates.
- Removed a redundant `value < 0` branch in the integer path; the pre-existing
  `delay < 0` check already covered both paths, and the `isdigit()` gate makes
  the string path unreachable for negatives.
- Restored `assertRaisesRegex(ValueError, "^TomTom response must be valid JSON$")`
  in the oversized-JSON-integer redaction test. The relaxation to bare
  `assertRaises` plus `assertNotIn("9", ...)` was unnecessary — the strict
  assertion passes against this branch's own parser — and it discarded the
  stable-error-contract assertion the redaction plan exists to protect.
- Added at-ceiling, ceiling-minus-one, and above-ceiling regressions for both
  integer and digit-string inputs. Verified they fail when the ceiling check is
  removed.

## Verification

- `python3 -m unittest tests.test_tomtom` — 18 tests, OK.
- Mutation: removing the `MAXIMUM_TOMTOM_DELAY_SECONDS` check fails 4 boundary
  cases, confirming the new coverage is load-bearing.
