# Finite Commute Settings

Status: planned

## Priority

P1 output integrity. Python floating-point parsing accepts `NaN` and infinity,
but those values do not represent usable commute distance, fuel economy, or
fuel cost and can render non-finite daily-cost output.

## Problem

`_positive_float()` rejects zero and negative values with `number <= 0`, but
that predicate accepts `NaN` because comparisons with `NaN` are false and also
accepts positive infinity. Directly constructed `MorningSettings` objects have
the same gap in `cost_per_day`.

## Approach

- Require parsed commute numeric settings to be finite and greater than zero.
- Keep the existing field-specific, value-redacting error messages.
- Apply the same finite positive invariant in `MorningSettings.cost_per_day` for
  direct callers.
- Add executable coverage for `NaN`, positive infinity, and negative infinity.
- Extend the dependency-free checker, maintained guidance, changelog, and plan
  completion evidence with mutation-sensitive contracts.

## Files

- `app.py`
- `tests/test_app.py`
- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-16-finite-commute-settings.md`

## Verification

- Run the focused settings tests and the complete offline unittest suite.
- Run all repository and external-directory Make gates.
- Reject isolated finite-check, direct-construction, test, guidance, changelog,
  and completed-plan mutations.
- Audit the exact diff, generated artifacts, credentials, conflict markers,
  binaries, large files, and whitespace.

## Scope Boundaries

- Do not change coordinate parsing, environment precedence, route behavior,
  TomTom transport, template output, dependencies, or hosted workflow shape.
- Do not expose rejected raw setting values in exceptions or documentation.
- Keep PR #16 and its predecessors open; this change is stacked and must retain
  base-first merge ordering.

## Success Criteria

- Settings loading rejects every non-finite commute numeric value with the same
  sanitized field-specific error used for other invalid positive values.
- Direct cost calculation rejects non-finite inputs before producing output.
- Ordinary finite positive commute costs remain unchanged.
