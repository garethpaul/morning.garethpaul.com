# Positive Commute Settings Plan

status: completed

## Context

`load_settings` parsed commute distance, fuel economy, and fuel cost as floats,
but zero or negative values could still be accepted and produce impossible or
misleading commute-cost output.

## Objectives

- Preserve numeric parsing errors for non-numeric commute settings.
- Reject non-positive `work_miles`, `miles_per_gallon`, and `cost_per_gallon`
  values during settings loading.
- Keep `MorningSettings.cost_per_day` guarded for direct construction in tests
  or callers.
- Cover non-positive commute settings with offline unit tests.
- Extend `make check` so future settings changes keep positive numeric
  validation.

## Verification

- `make check`
- `python3 -m unittest discover -s tests`
- `python3 scripts/check-baseline.py`
- `git diff --check`
