# TomTom Invalid Encoding Redaction

status: completed

## Context

The TomTom parser converts string and byte payloads with `json.loads()` and
redacts `JSONDecodeError`, but invalid UTF-8 bytes raise `UnicodeDecodeError`
instead. That exception retains the raw response bytes and bypasses the stable
credential- and body-redacted parser boundary.

## Requirements

- Map invalid UTF-8 and malformed JSON payloads to the same stable parser error.
- Do not retain an exception cause or context containing the response body.
- Preserve mapping payloads, valid string/byte JSON, delay validation, response
  size limits, and transport error handling.
- Add focused mutation-sensitive tests, checker contracts, and synchronized
  documentation.

## Non-Goals

- Changing TomTom endpoints, request headers, timeouts, or credentials.
- Contacting TomTom or adding parser dependencies.
- Changing route-summary or delay-value semantics.

## Verification Plan

- Run the focused TomTom tests, all four Make gates, and the external-directory
  Make gate with bytecode disabled.
- Reject invalid-encoding catch, stable message, cause/context, focused-test,
  documentation, and plan-evidence mutations.
- Audit the exact diff, generated artifacts, dependency files, secrets,
  conflict markers, and changed-line credential patterns.
- Capture one bounded exact-head pull-request and security snapshot after push.

## Work Completed

- Included `UnicodeDecodeError` in the existing two-phase parser failure
  boundary so invalid bytes map to the stable JSON validation message.
- Preserved a cause- and context-free raise outside the decoder handler so raw
  response bytes are not retained by application diagnostics.
- Added focused byte-payload coverage and synchronized static and documentation
  contracts.

## Verification Completed

- The focused `test_tomtom.py` discovery run passed all 11 tests.
- All four Make gates passed from the repository.
- The external-directory Make gate passed through the absolute Makefile path.
- Python compilation passed with cache output redirected outside the checkout.
- Six isolated hostile mutations were rejected across the invalid-encoding
  catch, stable message, cause/context boundary, focused test, documentation,
  and plan evidence.
- `git diff --check`, generated-artifact inspection, dependency-file review,
  conflict-marker review, secret scan, and changed-line credential-pattern
  review passed.
- No TomTom endpoint or external service was contacted.
