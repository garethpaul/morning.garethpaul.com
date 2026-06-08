# Issue 2 Disable Debug Mode

## Issue

`garethpaul/morning.garethpaul.com#2` reports that `app.py` enables Flask
debug mode unconditionally.

## Plan

- Default debug mode to false.
- Allow local development debug mode only through `MORNING_DEBUG`.
- Pass the explicit debug flag to `app.run`.
- Add tests that import the app with fake Flask/settings/tomtom dependencies.
- Add a source-level baseline check.

## Verification

- `python3 app_tests.py`
- `python3 -m py_compile app.py app_tests.py`
- `scripts/check-baseline.sh`
- `git diff --check`
