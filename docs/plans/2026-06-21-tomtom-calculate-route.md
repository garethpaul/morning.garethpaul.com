# TomTom Calculate Route Migration

status: completed

## Goal

Replace the non-resolving legacy TomTom route request and response shape with
the current Calculate Route contract while preserving credential-free offline
tests, bounded response handling, and stable error boundaries.

## Scope

- Request `https://api.tomtom.com/routing/1/calculateRoute/{locations}/json`
  with the configured key, traffic enabled, and the fastest route type.
- Parse `routes[0].summary.trafficDelayInSeconds` without accepting the legacy
  response shape.
- Reject missing or malformed routes, summaries, and delay fields through a
  stable body-free validation error.
- Document that the repository name is historical, no deployment configuration
  is included, and live local use requires coordinates plus `TOMTOM_API_KEY`.

## TDD Sequence

1. Prove the legacy endpoint fails the exact current URL assertion.
2. Prove the legacy response parser fails the current response fixture.
3. Prove malformed route layers retain internal exceptions, then remove that
   exception context.
4. Prove the request still sends a legacy referer, then remove it.

## Boundaries

- No authenticated TomTom request or real credential.
- No deployment configuration or domain changes.
- No dependency, Flask, template, or unrelated modernization changes.

## Verification

- All 13 TomTom tests passed with the cached Python 3.12 interpreter and
  existing Requests installation.
- All three Make root-authority tests passed.
- Static baseline, source compilation, `make lint`, `make build`, `actionlint`,
  `git diff --check`, and compiled-artifact checks passed.
- The complete Flask test module and therefore `make test` / `make check` could
  not run because no local interpreter had Flask installed. No dependency was
  downloaded or installed.
- No live or authenticated TomTom request was made.
