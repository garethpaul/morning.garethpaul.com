## Morning GarethPaul.com Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

Morning GarethPaul.com is a small Flask app that checks commute traffic and
renders morning commute information, including estimated delay and fuel cost.

The repository is useful as a personal commute dashboard sample using Flask,
TomTom route data, environment-backed local settings, and a simple web UI.
Project setup notes live in [`README.md`](README.md).

The goal is to keep the dashboard simple, credential-safe, and explicit about
location configuration.

Current baseline: `make lint`, `make test`, `make build`, and `make check`
cover offline unit tests, Python compilation, and `scripts/check-baseline.py`
verification for placeholder-safe settings, TomTom HTTPS URLs, fixture-based
route parsing, and `FLASK_DEBUG` opt-in behavior, plus positive numeric commute
settings.
Sanitized numeric setting errors keep invalid local configuration values out of
exception text.
TomTom JSON response validation keeps malformed route-service responses on a
stable parser error path before delay parsing.
TomTom delay value validation keeps parsed route delays on a non-negative
integer contract.
The bounded TomTom response keeps decompressed content entering JSON parsing at
or below 1 MiB and closes the HTTP response deterministically.
TomTom parser error redaction keeps malformed provider response bodies out of
the exception chain exposed to application diagnostics.
TomTom invalid encoding redaction keeps raw invalid UTF-8 provider bytes out of
that same exception chain.
Reviewed Python 3.12 dependency constraints keep hosted resolution stable while
using the patched Flask 3.1 line and preserving the requests 2.x compatibility
range. They do not authenticate downloaded artifacts with hashes.

The current focus is:

Priority:

- Preserve commute-delay and fuel-cost display behavior
- Keep home/work coordinates in environment variables or ignored local settings
- Keep placeholder settings importable without real commute values
- Keep coordinate setting validation before TomTom URL construction
- Keep coordinate tokens in provider-compatible ASCII decimal notation
- Keep coordinate range validation before TomTom URL construction
- Keep coordinate whitespace normalization after validation and before TomTom
  URL construction
- Keep TomTom API key placeholder validation before live route requests
- Keep TomTom JSON response validation before route delay parsing
- Keep TomTom delay value validation before rendering route delay data
- Keep the bounded TomTom response before JSON parsing
- Keep TomTom transport error redaction before request or cleanup failures reach logs
- Keep TomTom parser error redaction around malformed JSON validation
- Keep positive numeric commute settings for distance, MPG, and fuel cost
- Keep finite positive commute settings across loading and direct cost calculation
- Keep settings import error preservation for failures inside local configuration
- Keep sanitized numeric setting errors from echoing raw local values
- Keep lint, test, build, and check gates mapped to the offline baseline
- Keep check target gate order delegated through lint, test, and build
- Keep repository-relative Flask assets independent of the process working directory
- Keep Flask debug mode opt-in through `FLASK_DEBUG`
- Avoid committing API keys, location coordinates, or personal commute details
- Maintain security policy and Python/Flask context

Next priorities:

- Add weather or news inputs behind the same fixture-first testing approach
- Keep pinned, read-only Python 3.12 hosted validation covering dependency
  installation through the reviewed constraints graph, `pip check`, and
  offline route tests without TomTom access
- Document deployment environment variables for any hosted deployment

Contribution rules:

- One PR = one focused route, settings, UI, or documentation change.
- Do not commit personal coordinates or route API credentials.
- Run `make lint`, `make test`, `make build`, and `make check` before pushing
  source or documentation changes.
- Verify parsing with fixtures before live route calls.
- Document external route-service changes.
- Preserve positive numeric commute settings validation when changing cost logic.
- Preserve finite positive commute settings validation so `NaN` and infinity
  cannot become rendered fuel costs.
- Preserve coordinate range validation when changing route settings parsing.
- Preserve sanitized numeric setting errors when changing configuration parsing.
- Preserve repository-relative Flask assets when changing the app factory.

## Security And Privacy

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Home and work coordinates are sensitive. They must stay out of git, and logs
should avoid recording precise routes or commute patterns. Hosted deployments
should not enable Flask debug mode.
Repository-relative Flask assets should keep checked-in static files and
templates available regardless of the process working directory.

## What We Will Not Merge (For Now)

- Personal coordinates or route API keys
- Debug-mode production deployment
- Live-only tests as the default quality gate
- Broad rewrites without preserving the simple dashboard behavior

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
