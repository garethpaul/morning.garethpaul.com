# Hosted Python Validation

status: completed

## Context

The repository has dependency metadata, offline Flask and TomTom tests,
compilation checks, and a canonical local gate, but no hosted validation.

## Priorities

1. Install and validate declared dependencies on Python 3.12.
2. Run the canonical `make check` gate on hosted Linux.
3. Enforce a pinned, read-only, bounded workflow from the baseline checker.
4. Keep TomTom credentials, personal coordinates, and live route calls out of CI.

## Implementation Units

### Workflow And Checker

Files:

- `.github/workflows/check.yml`
- `scripts/check-baseline.py`

Add push, pull-request, and manual triggers; read-only permissions; concurrency
cancellation; a bounded `ubuntu-24.04` job; commit-pinned checkout and Python
setup; dependency caching; requirements installation; `pip check`; and
`make check`. Require that contract from the baseline checker.

### Documentation

Files:

- `README.md`
- `VISION.md`
- `SECURITY.md`
- `CHANGES.md`
- `docs/plans/2026-06-10-hosted-python-validation.md`

Document hosted dependency and offline route validation without implying a live
TomTom integration test.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- workflow YAML parse
- `git diff --check`
- successful hosted Linux `Check` workflow for the pushed commit

## Boundaries

- Do not provide TomTom keys, personal coordinates, or local settings files.
- Do not contact the TomTom API in CI.
