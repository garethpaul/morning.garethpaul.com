---
title: Issue 3 TomTom Timeout
type: fix
status: active
date: 2026-06-08
origin: https://github.com/garethpaul/morning.garethpaul.com/issues/3
execution: code
---

# Issue 3 TomTom Timeout

## Summary

Add a bounded timeout to the TomTom route request so the morning app does not
hang indefinitely when the upstream service stalls.

## Problem Frame

Issue #3 was filed because `stuff/tomtom.py` calls `urllib2.urlopen(request)`
without a timeout. Python defaults to waiting indefinitely.

## Requirements

- R1. Define an explicit timeout constant.
- R2. Pass the timeout to the TomTom `urlopen` call.
- R3. Keep the existing Python 2 request flow intact.
- R4. The PR must reference `https://github.com/garethpaul/morning.garethpaul.com/issues/3`.

## Implementation Unit

### U1. TomTom Timeout

- **Goal:** Add `URL_TIMEOUT_SECONDS`, pass it to `urllib2.urlopen`, and test
  that `getDelay` sends the timeout through a fake `urllib2` module.
- **Files:** `stuff/tomtom.py`, `tomtom_timeout_tests.py`,
  `scripts/check-baseline.sh`
- **Test Scenarios:** `getDelay` returns the parsed delay from a fake response
  and calls `urlopen` with `URL_TIMEOUT_SECONDS`; source checks reject the bare
  `urllib2.urlopen(request)` call.
- **Verification:** `python3 tomtom_timeout_tests.py`, `python3 -m py_compile
  stuff/tomtom.py tomtom_timeout_tests.py`, `scripts/check-baseline.sh`, and
  `git diff --check`.
