---
title: Python Dependency Constraints
date: 2026-06-12
status: completed
execution: code
---

# Python Dependency Constraints

## Context

`requirements.txt` exposed Flask 2.x and requests 2.x ranges, but the Python
3.12 workflow resolved those direct requirements and all transitive
dependencies afresh. The initial reviewed resolution selected Flask 2.3.3;
`pip-audit` then identified `CVE-2026-27205` / `GHSA-68rp-wp8r-4726`, whose
first patched release is Flask 3.1.3. Deterministic resolution must therefore
include the maintained patched Flask 3.1 line rather than freeze a known
vulnerability.

## Priorities

1. Move the Flask compatibility range to patched `>=3.1.3,<3.2` while
   preserving the requests 2.x compatibility range.
2. Add one reviewed constraints artifact for the complete Python 3.12 graph.
3. Install through the constraints artifact in GitHub Actions and invalidate
   the pip cache when either dependency file changes.
4. Make the dependency-free checker reject graph, workflow, cache,
   documentation, and completed-evidence drift.
5. Document that version constraints reduce resolver drift but do not
   authenticate downloaded artifacts.

## Implementation Units

### Dependency Graph

Files:

- `requirements.txt`
- `constraints.txt`

Keep Flask and requests as public compatibility ranges, with Flask restricted
to the patched 3.1 line. Record every direct and transitive package selected by
a clean Python 3.12 resolution in `constraints.txt` without adding unrelated
dependencies.

### Hosted Installation

File: `.github/workflows/check.yml`

Apply the constraints file to the sole dependency installation and include
both dependency files in setup-python's pip cache key. Preserve the pinned,
read-only, timeout-bounded workflow and both canonical events. Make the stated
credential-free boundary explicit with `persist-credentials: false` on the
sole checkout step and enforce that exact shape statically.

### Static Contract And Documentation

Files:

- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-12-python-dependency-constraints.md`

Require the exact reviewed graph, direct ranges, constrained install, cache
inputs, documentation boundary, completed status, and exact verification
evidence. Keep the checker dependency-free.

## Verification

- Resolve the direct ranges in a clean Python 3.12 environment and confirm the
  complete exact graph.
- Verify selected releases against official PyPI metadata.
- Install through `requirements.txt` and `constraints.txt`, then run
  `python -m pip check`.
- Run `make lint`, `make test`, `make build`, and `make check`.
- Exercise hostile mutations for graph drift, range drift, unconstrained or
  duplicate installation, cache drift, documentation drift, and stale plan
  evidence.
- Run Python compilation and `git diff --check`.
- Require successful push, pull-request, and CodeQL checks on the exact final
  head before tracker reconciliation.

## Boundaries

- Do not change dashboard, TomTom, settings, route, or template behavior.
- Do not narrow the requests 2.x compatibility range.
- Do not retain a Flask release affected by `CVE-2026-27205`.
- Do not claim hash-locked or offline-reproducible installation.
- Do not merge or close existing pull requests without explicit authorization.

## Work Completed

- Moved Flask to the patched `>=3.1.3,<3.2` line after the vulnerability audit
  identified `CVE-2026-27205`, preserved the requests compatibility range, and
  added the reviewed 12-package Python 3.12 constraints graph.
- Applied the graph to the sole hosted installation and included both
  dependency files in setup-python's pip cache key.
- Disabled checkout credential persistence explicitly and extended the
  dependency-free checker to enforce the exact workflow shape.
- Updated setup, security, vision, and change guidance without changing
  dashboard or TomTom runtime behavior.

## Verification Completed

- GitHub's reviewed `GHSA-68rp-wp8r-4726` advisory identified Flask `<3.1.3`
  as vulnerable and `3.1.3` as the first patched version.
- Official PyPI metadata verified non-yanked release artifacts and compatible
  Python metadata for every package in the patched 12-package graph.
- Resolver dry runs for Python 3.10, 3.12, and 3.14 selected the same exact
  graph recorded in `constraints.txt`.
- An isolated Python 3.12.8 environment installed through `requirements.txt`
  and `constraints.txt`; `python -m pip check` reported no broken
  requirements.
- `pip-audit -r constraints.txt --no-deps` reported no known vulnerabilities
  after Flask moved to 3.1.3.
- `make test` passed all 17 offline tests and `make build` completed Python
  compilation successfully.
- `make lint`, `make test`, `make build`, and `make check` passed; checker
  compilation and `git diff --check` also passed.
- Fourteen focused hostile mutations were rejected across the vulnerable Flask
  range and pin, graph removal or addition, requests-range drift,
  unconstrained or duplicate installation, cache drift, credential
  persistence, duplicate checkout, documentation drift, status regression,
  advisory evidence drift, and vulnerability-audit evidence drift.
- Implementation head `1adf9d43e3dcea2fb211ea3318d56bc90c610ac5`
  passed push Check run `27437919847`, pull-request Check run `27437931925`,
  and CodeQL run `27437930574` for Actions and Python.
- Pull request #12 was open, clean, and mergeable at that implementation head
  with all five exact-head checks successful and zero open PR-scoped
  code-scanning alerts.
