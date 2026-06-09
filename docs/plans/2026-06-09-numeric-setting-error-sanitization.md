# Numeric Setting Error Sanitization

status: completed

## Context

Commute numeric settings are loaded from environment variables or ignored local
settings files. Non-numeric values previously chained Python's conversion error,
which could expose the raw local configuration value through exception causes.

## Goals

- Keep field-specific errors for non-numeric commute settings.
- Suppress raw conversion exceptions with `from None`.
- Cover the behavior with offline unit tests.
- Document and preserve the sanitization in the static baseline.

## Verification

- `python3 -m unittest discover -s tests`
- `python3 scripts/check-baseline.py`
- `make check`
- `git diff --check`
