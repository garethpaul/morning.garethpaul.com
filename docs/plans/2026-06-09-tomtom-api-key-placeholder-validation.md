# TomTom API Key Placeholder Validation

status: completed

## Context

`settings.py.example` documents `TOMTOM_API_KEY` with a placeholder value. A
copied local settings file or environment variable should not treat that
placeholder as a configured key before constructing live TomTom route requests.

## Objectives

- Reject copied TomTom API key placeholders before live route requests.
- Keep errors limited to the setting name without echoing configured key values.
- Preserve existing environment and local settings precedence.
- Extend tests, static baseline, and docs for TomTom API key placeholder
  validation.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
