# morning.garethpaul.com

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/morning.garethpaul.com` is a small Flask commute dashboard. It checks TomTom route delay data, renders a morning travel page, and estimates daily commute fuel cost.

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Python (5).

## Repository Contents

- `README.md` - project overview and local usage notes
- `.gitignore` - local settings and Python artifact ignores
- `CHANGES.md` - recent maintenance changes
- `Makefile` - local static verification entry point
- `app.py` - Flask app factory and runtime settings loader
- `requirements.txt` - patched Flask 3.1 and requests 2.x compatibility ranges
- `constraints.txt` - reviewed exact Python 3.12 dependency graph used by CI
- `SECURITY.md` - security reporting and disclosure guidance
- `scripts/check-baseline.py` - static commute dashboard baseline checks
- `static` - source or example code
- `stuff` - source or example code
- `templates` - source or example code
- `tests` - offline unit tests for config, routes, and TomTom parsing
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: static, stuff, templates
- Dependency and build manifests: requirements.txt, constraints.txt
- Entry points or build surfaces: `make lint`, `make test`, `make build`, `make check`, app.py
- Test-looking files: tests/test_app.py, tests/test_tomtom.py

## Getting Started

### Prerequisites

- Git
- Python 3.10 or newer
- Flask and requests from `requirements.txt` and `constraints.txt`

### Setup

```bash
git clone https://github.com/garethpaul/morning.garethpaul.com.git
cd morning.garethpaul.com
python3 -m pip install -r requirements.txt -c constraints.txt
make lint
make test
make build
make check
cp settings.py.example settings.py
```

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

## Running or Using the Project

- Copy `settings.py.example` to `settings.py` or set the documented environment variables before making live TomTom requests.
- Run `python app.py` for local development.
- For Flask CLI usage, set `FLASK_APP=app:create_app`.
- Set `FLASK_DEBUG=1` only for local debugging.
- Repository-relative Flask assets keep `static/` and `templates/` resolved
  from the checked-in app directory even when the process starts elsewhere.

## Testing and Verification

- `make lint` runs `scripts/check-baseline.py`, `make test` runs offline unit
  tests, `make build` compiles Python files, and `make check` runs the full
  clean/lint/test/build gate.
- The Make gates are location-independent. From another directory, pass the
  checkout's Makefile by absolute path, such as
  `make -f /path/to/morning.garethpaul.com/Makefile check`.
- Check target gate order keeps the full local gate delegated through the same
  named lint, test, and build targets used before pushing.
- Pinned, credential-free `ubuntu-24.04` GitHub Actions installs
  `requirements.txt` through the reviewed versions in `constraints.txt`, runs
  `pip check`, and executes `make check` on Python 3.12. Hosted tests use
  fixtures and injected HTTP calls without a TomTom key, personal coordinates,
  local settings, or live route requests.
- The constraints freeze the reviewed direct and transitive versions, but they
  do not authenticate downloaded package artifacts with hashes.
- Flask stays on `>=3.1.3,<3.2` because 3.1.3 is the first release patched for
  `CVE-2026-27205` / `GHSA-68rp-wp8r-4726`.
- `python3 -m unittest discover -s tests` verifies configuration, Flask routes, TomTom URL construction, response parsing, and injected HTTP behavior without live TomTom calls.
- Offline tests also cover repository-relative Flask assets so `/static/styles.css`
  remains available when `create_app` runs from another working directory.
- Offline tests cover TomTom JSON response validation so malformed route-service
  responses fail with stable parser errors.
- The bounded TomTom response reader streams at most 1 MiB of decompressed
  content into JSON parsing and closes responses on success or failure.
- TomTom transport error redaction converts Requests transport and HTTP status
  failures to a stable message without retaining the API-key-bearing URL.
- TomTom parser error redaction raises malformed-JSON failures outside the
  decoder handler so provider response bodies are not retained in exceptions.
- TomTom invalid encoding redaction maps invalid UTF-8 response bytes to the
  same stable parser error without retaining the body in exception context.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- Home/work coordinates, route API keys, personal commute details, `.env` files, and local settings overlays should stay out of git.
- `settings.py.example` in this repository is a placeholder template; real values belong in local-only `settings.py` or another ignored local configuration file.
- Prefer environment variables: `MORNING_HOME_POS`, `MORNING_WORK_POS`, `MORNING_WORK_MILES`, `MORNING_MILES_PER_GALLON`, `MORNING_COST_PER_GALLON`, and `TOMTOM_API_KEY`.
- Coordinate setting validation requires `MORNING_HOME_POS` and `MORNING_WORK_POS` to be numeric coordinate pairs before TomTom URL construction.
- Coordinate range validation keeps latitude and longitude values within valid global bounds before TomTom URL construction.
- TomTom API key placeholder validation rejects copied template values before live route requests.
- TomTom JSON response validation rejects malformed route-service responses
  before reading delay fields.
- TomTom delay value validation accepts only non-negative integers or ASCII
  digit strings before rendering route delays.
- The bounded TomTom response rejects more than 1 MiB before JSON parsing;
  lower HTTP layers may still buffer transport data.
- Positive numeric commute settings are required for work miles, miles per gallon, and cost per gallon.
- Finite positive commute settings reject `NaN` and infinity before fuel-cost
  calculation or dashboard rendering.
- Sanitized numeric setting errors name the invalid field without echoing raw
  local configuration values.

## Security and Privacy Notes

- Review changes touching network requests, sockets, or service endpoints; examples from the scan include app.py, stuff/tomtom.py, templates/index.html.
- Keep TomTom requests on HTTPS and do not enable Flask debug mode in hosted deployments.
- Keep TomTom transport error redaction in place so request URLs containing the
  API key do not reach Flask or process-supervisor exception logs.
- Keep TomTom parser error redaction in place so malformed provider bodies do
  not remain reachable through chained decoder exceptions.
- Keep TomTom API key placeholder validation in place so copied templates fail before live route requests.
- Keep TomTom JSON response validation in place so malformed route responses
  fail before delay parsing.
- Keep TomTom delay value validation in place so booleans, fractional values,
  and negative delays do not reach the dashboard.
- Keep coordinate range validation in place so impossible home/work positions fail before live route requests.
- Keep positive numeric commute settings validation in place so the dashboard does not render impossible fuel-cost output.
- Keep finite positive commute settings validation in both loading and direct
  cost calculation so non-finite output cannot reach the dashboard.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include stuff/tomtom.py.
- Tests should use fixture responses and injected HTTP clients instead of live route calls.
- Keep repository-relative Flask assets in place so changing the process working
  directory cannot break checked-in templates or static files.

## Maintenance Notes

- Run `make lint`, `make test`, `make build`, and `make check` before pushing
  Python, TomTom, settings, template, dependency, or security documentation
  changes.
- Use an absolute Makefile path when running those gates outside the checkout.
- See `docs/plans/2026-06-08-morning-dashboard-baseline.md` for the current completed baseline plan.
- See `docs/plans/2026-06-09-make-gate-aliases.md` for the local gate alias
  baseline.
- See `docs/plans/2026-06-09-check-target-gate-order.md` for the check target
  gate order guardrail.
- See `docs/plans/2026-06-09-numeric-setting-error-sanitization.md` for the
  sanitized numeric setting errors guard.
- See `docs/plans/2026-06-09-repository-relative-flask-assets.md` for the
  repository-relative Flask assets guardrail.
- See `docs/plans/2026-06-10-tomtom-json-response-validation.md` for the
  TomTom JSON response validation guardrail.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
