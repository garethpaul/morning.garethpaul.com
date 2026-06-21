# Spaced Absolute Makefile Path Verification

status: completed

## Context

GNU Make list functions split a loaded absolute Makefile path at spaces. When
the checkout path contains spaces, brackets, and an apostrophe, the existing
root expression keeps only the final whitespace-delimited fragment and points
verification at the caller directory instead of the checkout.

## Scope

1. Derive the checkout root from the complete `MAKEFILE_LIST` value without
   treating filesystem whitespace as Make list syntax.
2. Ignore command-line and environment `ROOT` overrides.
3. Reject command-line or environment-preferred `MAKEFILE_LIST` overrides.
4. Exercise all eight Make aliases from an external working directory.

## Verification

- The full root and external-directory `make check` gates passed under
  `/bin/dash` from a path containing spaces, brackets, and an apostrophe.
- Offline regression tests dry-ran all eight Make aliases with no override,
  a command-line `ROOT` override, and an environment `ROOT` override.
- Command-line and environment-preferred `MAKEFILE_LIST` overrides failed
  closed before any recipe ran.
- Python warning-as-error compilation and `git diff --check` passed.

## Risk And Rollback

This changes verification root discovery only. Rollback restores the previous
Make expression and removes the hostile-path regression contract.
