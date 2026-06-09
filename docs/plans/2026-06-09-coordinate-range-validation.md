# Coordinate Range Validation

status: completed

## Context

`load_settings` validates home and work positions as numeric coordinate pairs
before TomTom URL construction. Numeric pairs outside valid latitude or
longitude ranges can still form impossible route requests while passing the
existing parser.

## Objectives

- Require latitude values to stay within `-90...90`.
- Require longitude values to stay within `-180...180`.
- Keep coordinate errors limited to setting names, not raw local values.
- Preserve existing environment-first settings loading.
- Extend tests, static checks, and docs for coordinate range validation.

## Verification

- `make check`
- `python3 -m unittest discover -s tests`
- `git diff --check`
