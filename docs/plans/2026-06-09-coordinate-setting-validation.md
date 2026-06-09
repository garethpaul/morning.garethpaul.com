# Coordinate Setting Validation Plan

status: completed

## Context

`load_settings` requires home and work positions, then passes them into TomTom
route URL construction. Missing values are rejected, but malformed non-numeric
coordinate strings could still reach request construction.

## Objectives

- Validate home and work positions as two-part numeric coordinate strings.
- Keep coordinate errors limited to setting names, not raw local values.
- Preserve existing environment-first settings loading.
- Extend unit tests, docs, and the static baseline for coordinate setting
  validation.

## Verification

- `make check`
- `python3 -m unittest discover -s tests`
- `git diff --check`
