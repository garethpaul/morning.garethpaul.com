# Morning Dashboard Make Gate Aliases

status: completed

## Context

The repository had `make check`, `make test`, `make compile`, and
`make static-check` targets, but the fleet pre-push sequence also invokes
`make lint` and `make build`. Those commands should reach the existing offline
checks instead of failing before the Python baseline runs.

## Objectives

- Expose lint, test, build, check, and verify Make targets.
- Map `make lint` to the static baseline.
- Map `make build` to Python compilation.
- Keep `make check` as the full clean/test/compile/static-check gate.
- Document and pin the target contract in the static checker.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `make verify`
- `git diff --check`
