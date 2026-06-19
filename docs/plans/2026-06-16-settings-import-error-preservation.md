# Settings Import Error Preservation

Status: completed

## Priority

P1 deployment diagnosability. An existing `settings.py` can fail because one of
its own imports is unavailable, but the application currently suppresses that
failure and reports unrelated missing configuration fields.

## Problem

`_load_optional_settings_module()` treats every `ModuleNotFoundError` raised by
`importlib.import_module("settings")` as proof that the optional settings module
does not exist. Python uses the same exception for dependencies imported from
inside `settings.py`, so a missing nested package is silently converted into a
misleading configuration error and loses the original module name and traceback.

## Requirements

- R1: Continue returning no module when the top-level optional `settings`
  module itself is absent.
- R2: Re-raise `ModuleNotFoundError` when an existing settings module fails to
  import another module.
- R3: Preserve environment-first configuration precedence and all current
  validation, redaction, route, and TomTom behavior.
- R4: Add executable and mutation-sensitive evidence for both import outcomes.

## Key Technical Decision

Use the exception's missing-module identity to distinguish an absent top-level
`settings` module from a nested import failure. This keeps the existing optional
module contract without filesystem probing, speculative imports, or broad
exception translation.

## Implementation Units

### U1: Preserve nested settings import failures

**Files:** `app.py`, `tests/test_app.py`

- Add a focused regression that simulates an absent top-level settings module.
- Add a regression that simulates a dependency missing from inside the settings
  module and proves the original exception remains visible.
- Narrow the optional import fallback to the exact top-level module absence.

**Test scenarios:**

- Importing `settings` raises `ModuleNotFoundError` naming `settings`: loading
  continues without a module and reports missing required settings normally.
- Importing `settings` raises `ModuleNotFoundError` naming a nested dependency:
  the same failure propagates with its missing dependency identity intact.
- A supplied settings object and environment overrides continue to load
  normally.

### U2: Lock the maintenance contract and evidence

**Files:** `scripts/check-baseline.py`, `README.md`, `SECURITY.md`, `VISION.md`,
`CHANGES.md`, `docs/plans/2026-06-16-settings-import-error-preservation.md`

- Add static contracts for selective exception handling and executable test
  coverage.
- Document why nested settings import failures must remain observable.
- Record completed local verification only after every required gate passes.

**Test scenarios:**

- The checker rejects broad suppression, a missing nested-import regression,
  stale guidance, or incomplete plan evidence.
- Repository and external-directory verification use the same checkout-rooted
  baseline.

## Scope Boundaries

- Do not change setting names, environment precedence, coordinate or numeric
  validation, API-key redaction, Flask routes, dependencies, or TomTom calls.
- Do not translate nested import failures into a new application exception;
  preserve Python's original diagnostic.
- Keep PR #17 and its predecessors open. This change is stacked and must retain
  base-first merge ordering.

## Verification

- Run focused settings tests and the complete offline unit suite.
- Run all repository and external-directory Make gates.
- Reject isolated mutations covering top-level absence, nested failure
  propagation, executable coverage, guidance, and completed plan evidence.
- Audit the exact diff, generated artifacts, credentials, conflict markers,
  binaries, large files, modes, and whitespace.

## Success Criteria

- Only absence of the optional top-level `settings` module is suppressed.
- Nested module import failures remain visible with their original identity.
- Existing configuration behavior and all offline tests remain green.

## Verification Completed

- The focused import-boundary regressions and all 24 offline tests passed.
- All four Make gates passed from the repository root, and the absolute
  Makefile `check` gate passed from an external directory.
- Seven isolated hostile mutations were rejected across selective exception
  handling, top-level absence, nested failure propagation, executable coverage,
  guidance, plan status, and plan evidence.
- Application, test, and checker compilation plus `git diff --check` passed.
- Exact intended-path, generated-artifact, credential-pattern, conflict-marker,
  binary, large-file, mode, and whitespace audits passed.
