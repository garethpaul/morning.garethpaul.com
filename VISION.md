## Morning GarethPaul.com Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

Morning GarethPaul.com is a small Flask app that checks commute traffic and
renders morning commute information, including estimated delay and fuel cost.

The repository is useful as a personal commute dashboard sample using Flask,
TomTom route data, local settings, and a simple web UI. Project setup notes live
in [`README.md`](README.md).

The goal is to keep the dashboard simple, credential-safe, and explicit about
location configuration.

The current focus is:

Priority:

- Preserve commute-delay and fuel-cost display behavior
- Keep home/work coordinates in local settings rather than public source
- Avoid committing API keys, location coordinates, or personal commute details
- Maintain security policy and old Python/Flask context

Next priorities:

- Move coordinates and route-service configuration into ignored local config
- Port to supported Python and maintained HTTP libraries
- Add tests with fixture route responses
- Disable debug mode for any hosted deployment notes

Contribution rules:

- One PR = one focused route, settings, UI, or documentation change.
- Do not commit personal coordinates or route API credentials.
- Verify parsing with fixtures before live route calls.
- Document external route-service changes.

## Security And Privacy

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Home and work coordinates are sensitive. They must stay out of git, and logs
should avoid recording precise routes or commute patterns.

## What We Will Not Merge (For Now)

- Personal coordinates or route API keys
- Debug-mode production deployment
- Live-only tests as the default quality gate
- Broad rewrites without preserving the simple dashboard behavior

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
