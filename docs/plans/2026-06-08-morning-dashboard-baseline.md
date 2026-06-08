# Morning Dashboard Baseline Plan

status: completed

## Context

`morning.garethpaul.com` is a small Flask commute dashboard. It previously
imported a local `settings.py` at module import time, used Python 2 `urllib2`,
embedded a TomTom route API key in source, and had no automated tests or
dependency manifest.

## Risks

- Home/work coordinates and TomTom keys are sensitive and should not be tracked.
- Import-time local settings made offline tests and production imports brittle.
- Debug mode was enabled unconditionally for any `python app.py` run.
- Live route calls were the only way to exercise route parsing.

## Work Completed

- Added explicit settings loading from environment variables with an ignored
  `settings.py` fallback and a safe `settings.py.example` template.
- Moved the TomTom key into `TOMTOM_API_KEY` and switched route calls to HTTPS
  through `requests`.
- Added an app factory so tests can inject a fake traffic client.
- Added fixture-style unit tests for configuration, Flask routes, TomTom URL
  construction, response parsing, and injected HTTP behavior.
- Added `requirements.txt`, `Makefile`, and `scripts/check-baseline.py`.

## Verification

- `make check`
- `python3 -m unittest discover -s tests`
- `git diff --check`
