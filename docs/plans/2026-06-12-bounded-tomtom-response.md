# Bounded TomTom Response

status: planned

## Context

The TomTom client reads `response.text`, which can materialize an unexpectedly
large response before JSON validation and does not deterministically close the
HTTP response. The request already has a timeout and strict status, JSON shape,
and delay-value checks, but parser input remains unbounded.

## Priorities

1. Stream at most 1 MiB plus an overflow byte into the JSON parser.
2. Reject oversized responses without including response content in the error.
3. Close the HTTP response on status, read, parse, and success paths.
4. Verify behavior with injected offline response fakes.

## Implementation Units

### TomTom Client

File: `stuff/tomtom.py`

Request streaming responses, accumulate bounded decompressed chunks, reject an
overflow byte, and close the response in a `finally` block. Keep the existing
10-second timeout, status check, route construction, and parser contracts.

### Offline Tests

File: `tests/test_tomtom.py`

Assert streaming request options, exact successful reads, oversize rejection,
and deterministic closure on success and failure.

### Static Contract And Documentation

Files:

- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-12-bounded-tomtom-response.md`

Protect the response boundary and document that it limits decompressed content
entering JSON parsing rather than all buffering in the HTTP stack.

## Verification

- `python3 -m py_compile stuff/tomtom.py tests/test_tomtom.py scripts/check-baseline.py`
- focused TomTom tests
- `make lint`
- `make test`
- `make build`
- `make check`
- hostile mutations removing the overflow probe or response closure
- `git diff --check`
- hosted push and pull-request checks

## Boundaries

- Do not make live TomTom requests in tests or CI.
- Do not change endpoint, timeout, route direction, or delay semantics.
- Do not include response bodies or API keys in errors.
