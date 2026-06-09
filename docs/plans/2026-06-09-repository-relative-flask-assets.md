# Repository-Relative Flask Assets

status: completed

## Context

`create_app` configured Flask static files from `os.getcwd()`. That works when
the process starts in the repository root, but it can point Flask at the wrong
directory when the app is imported by a runner, CLI, or deployment from another
working directory.

## Objectives

- Resolve `static/` and `templates/` from the checked-in app directory.
- Keep the existing Flask app factory and route behavior unchanged.
- Add an offline test that changes the process working directory and still
  fetches `/static/styles.css`.
- Extend the static baseline and docs so asset path resolution stays
  repository-relative.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
