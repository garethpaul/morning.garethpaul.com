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

The current focus is:

Priority:

- Preserve commute-delay and fuel-cost display behavior
- Keep home/work coordinates in environment variables or ignored local settings
- Keep placeholder settings importable without real commute values
- Keep coordinate setting validation before TomTom URL construction
- Keep TomTom API key placeholder validation before live route requests
- Keep positive numeric commute settings for distance, MPG, and fuel cost
- Keep sanitized numeric setting errors from echoing raw local values
- Keep lint, test, build, and check gates mapped to the offline baseline
- Keep Flask debug mode opt-in through `FLASK_DEBUG`
- Avoid committing API keys, location coordinates, or personal commute details
- Maintain security policy and Python/Flask context

Next priorities:

- Add weather or news inputs behind the same fixture-first testing approach
- Add CI once the repository owner wants verification on every push
- Document deployment environment variables for any hosted deployment

Contribution rules:

- One PR = one focused route, settings, UI, or documentation change.
- Do not commit personal coordinates or route API credentials.
- Run `make lint`, `make test`, `make build`, and `make check` before pushing
  source or documentation changes.
- Verify parsing with fixtures before live route calls.
- Document external route-service changes.
- Preserve positive numeric commute settings validation when changing cost logic.
- Preserve sanitized numeric setting errors when changing configuration parsing.

## Security And Privacy

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Home and work coordinates are sensitive. They must stay out of git, and logs
should avoid recording precise routes or commute patterns. Hosted deployments
should not enable Flask debug mode.

## What We Will Not Merge (For Now)

- Personal coordinates or route API keys
- Debug-mode production deployment
- Live-only tests as the default quality gate
- Broad rewrites without preserving the simple dashboard behavior

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
