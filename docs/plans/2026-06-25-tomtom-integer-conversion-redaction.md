# TomTom Integer Conversion Redaction

status: completed

## Context

Python 3.12 limits decimal integer conversion length. A TomTom response with an
oversized JSON integer raised Python's raw `ValueError` instead of the stable
parser error, while an oversized ASCII digit string retained that conversion
exception as its cause.

## Requirements

- Map oversized JSON integers to the stable malformed-JSON error.
- Map oversized digit strings to the stable delay-value error.
- Publish both errors outside their conversion handlers so cause and context
  do not retain provider response details.
- Preserve valid delay values, response limits, transport handling, and route
  response-shape validation.

## Work Completed

- Expanded the JSON conversion boundary to include plain `ValueError` from
  Python's integer-length limit.
- Deferred digit-string conversion failures until after the conversion handler.
- Added focused cause- and context-free regressions for both oversized forms.
- Extended static contracts, documentation, and change history.

## Verification Completed

- The focused oversized-integer regressions passed after failing against the
  previous conversion paths.
- `make lint`, `make test`, `make build`, and `make check` passed with no live
  TomTom requests.
- `git diff --check` passed.

## Scope Boundaries

- No endpoint, credential, timeout, response-size, or accepted delay semantics changed.
- No provider response content is logged or persisted.
