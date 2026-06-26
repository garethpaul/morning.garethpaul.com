# TomTom Degraded Dashboard

status: completed

## Problem

Both Flask routes called the injected TomTom client directly. Stable transport,
cleanup, bounded-response, encoding, JSON, schema, and delay validation failures
therefore replaced the whole dashboard with Flask's generic 500 response even
though local fuel-cost and news content remained available.

## Scope

- Convert only `RuntimeError` and `ValueError`, the documented TomTom transport
  and parser surface, into an explicit redacted unavailable state.
- Preserve HTTP 200 dashboard rendering, local fuel-cost content, route choice,
  settings, and existing successful delay output.
- Let unexpected exceptions such as `TypeError` continue to propagate so code
  defects are not hidden.
- Do not log or render provider exception messages, credentials, coordinates,
  response bodies, or chained details.

## Verification

- Add red tests proving both expected failure classes currently return 500.
- Add work and home route assertions for status 200, unavailable text, retained
  local content, and absence of a private provider token.
- Add a focused assertion that unexpected `TypeError` still propagates.
- Run `make check` in the reviewed Python 3.12 constraints environment.
- Run isolated hostile mutations for removed catches, broad catches, missing
  template state, hidden unexpected errors, and leaked provider details.
- Require exact-head hosted Python 3.12 and CodeQL checks before merge.

## Boundary

This change does not add retries, caching, live TomTom calls, new credentials,
deployment configuration, weather/news services, persistence, or logging. It
does not claim the provider is healthy; it keeps the local dashboard usable
while clearly marking traffic delay data unavailable.
