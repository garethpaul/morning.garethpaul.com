# Morning Baseline Plan

status: completed

## Context

`morning.garethpaul.com` is a small Flask commute dashboard that reads local commute settings, checks TomTom route delay, and renders a simple morning page. The original code had no local verification command and assumed real numeric settings at import time.

## Objectives

- Add a static `make check` path that does not need Flask or live TomTom access.
- Keep home/work coordinates and local settings out of public source.
- Keep committed settings placeholders in `settings.py.example`.
- Make placeholder numeric settings safe for import and local checks.
- Keep Flask debug mode disabled unless explicitly requested.
- Use HTTPS for route-service and template asset URLs.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
