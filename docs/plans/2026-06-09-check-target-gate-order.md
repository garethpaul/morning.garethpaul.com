# Check Target Gate Order

status: completed

## Context

The repository exposed `make lint`, `make test`, `make build`, and `make check`,
but `make check` still duplicated the underlying test, compile, and static-check
commands instead of delegating through the named gates. The shared workflow
expects those gate names to be the path used before pushing.

## Objectives

- Keep `make lint` as the static baseline gate.
- Keep `make test` as the offline unit test gate.
- Keep `make build` as the Python compilation gate.
- Make `make check` clean generated artifacts and then run lint, test, and
  build through the named targets.
- Update documentation so the full gate order is visible.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
