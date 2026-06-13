# Location-Independent Morning Dashboard Verification

status: in progress

## Context

Absolute Makefile invocations run tests, compilation, static checks, and cleanup
against the caller's directory instead of the checkout, so documented gates
fail or inspect the wrong tree outside the repository.

## Scope

1. Derive the checkout root from the loaded Makefile.
2. Run tests, compilation, static checks, verification, and bytecode cleanup
   from that root.
3. Add exact Makefile, completed-plan, external-run, and guidance contracts.
4. Preserve TomTom validation and redaction, Flask assets, dependency
   constraints, workflow policy, and all existing stacked artifacts.

## Verification Plan

- Run every non-mutating Make gate from the checkout and through an absolute
  Makefile path from a temporary directory; verify cleanup remains root-scoped.
- Run the full offline suite, checker compilation, module compilation,
  dependency constraints, and diff checks.
- Reject root derivation, test, compile, checker, cleanup, plan status/evidence,
  and documentation mutations independently.
- Inspect intended paths, secret patterns, conflict markers, generated
  artifacts, and Python/runtime/workflow changes before commit.

## Risk And Rollback

This changes verification path resolution only. Rollback restores the relative
recipes and removes their checker, plan, and documentation contracts.
