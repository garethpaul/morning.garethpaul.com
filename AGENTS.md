# AGENTS.md

## Repository purpose

`garethpaul/morning.garethpaul.com` is a small Flask commute dashboard. It checks TomTom route delay data, renders a morning travel page, and estimates daily commute fuel cost.

## Project structure

- `Makefile` - location-independent repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `tests` - offline unit tests and fixtures
- `templates` - server-rendered templates
- `requirements.txt` - direct Python compatibility ranges
- `constraints.txt` - reviewed exact Python 3.12 dependency graph used by CI

## Development commands

- Install dependencies: `python3 -m pip install -r requirements.txt -c constraints.txt`
- Full baseline: `make check`
- Combined verification: `make verify`
- Lint/static checks: `make lint`
- Tests: `make test`
- Build: `make build`
- From another directory: `make -f /path/to/morning.garethpaul.com/Makefile check`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- The application and its tests use Python; workflow and repository automation use Make and YAML.
- Prefer dependency-free tests or stdlib checks when legacy packages are unavailable.
- Keep hosted CI pinned, credential-free, constrained, and bounded to `make check`.

## Testing guidance

- Test-related files: `tests/test_app.py`, `tests/test_tomtom.py`, `tests/test_check_baseline.py`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- Home/work coordinates, route API keys, personal commute details, `.env` files, and local settings overlays should stay out of git.
- `settings.py.example` in this repository is a placeholder template; real values belong in local-only `settings.py` or another ignored local configuration file.
- Prefer environment variables: `MORNING_HOME_POS`, `MORNING_WORK_POS`, `MORNING_WORK_MILES`, `MORNING_MILES_PER_GALLON`, `MORNING_COST_PER_GALLON`, and `TOMTOM_API_KEY`.
- Coordinate setting validation requires `MORNING_HOME_POS` and `MORNING_WORK_POS` to be numeric coordinate pairs before TomTom URL construction.
- Coordinate range validation keeps latitude and longitude values within valid global bounds before TomTom URL construction.
- TomTom API key placeholder validation rejects copied template values before live route requests.
- Never commit live TomTom credentials, personal coordinates, or local settings.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
