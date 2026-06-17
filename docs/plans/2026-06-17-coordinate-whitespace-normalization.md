---
title: "fix: Normalize validated commute coordinates"
type: fix
status: planned
date: 2026-06-17
execution: code
---

# Normalize Validated Commute Coordinates

## Summary

Return canonical comma-separated coordinate components after numeric and range
validation so accepted whitespace around latitude or longitude cannot leak into
TomTom route URLs as encoded spaces.

## Problem Frame

`_coordinate_pair` accepts numeric components containing surrounding whitespace
because `float()` ignores it, but returns the original setting unchanged.
`route_url` then percent-encodes those spaces. The setting therefore passes the
repository's validation boundary yet produces a different provider path than
the validated numeric pair represents.

## Requirements

- R1. Strip surrounding whitespace independently from latitude and longitude
  components after splitting.
- R2. Preserve numeric text and component order while returning exactly one
  comma with no surrounding whitespace.
- R3. Keep existing shape, finite/range, environment precedence, and sanitized
  error behavior unchanged.
- R4. Prove normalized settings produce TomTom route URLs without encoded
  coordinate whitespace.
- R5. Add mutation-sensitive tests, static contracts, guidance, and completed
  verification evidence.

## Key Technical Decisions

- KTD1. Preserve component text instead of reformatting through `float` output.
  This removes whitespace without changing decimal precision, signs, or valid
  exponent notation.
- KTD2. Normalize at settings validation rather than in `route_url`, so every
  downstream consumer receives the same validated canonical values.

## Scope Boundaries

- Do not change coordinate precision, provider endpoints, API-key handling,
  route direction, or TomTom request behavior beyond removing component-edge
  whitespace.
- Do not merge or close stacked pull requests without explicit authorization.

## Implementation Units

### U1. Canonicalize validated coordinate pairs

- **Files:** `app.py`
- **Requirements:** R1, R2, R3
- **Goal:** Validate stripped components and return their canonical comma join.

### U2. Prove settings-to-provider normalization

- **Files:** `tests/test_app.py`, `tests/test_tomtom.py`,
  `scripts/check-baseline.py`
- **Requirements:** R2, R3, R4, R5
- **Scenarios:** Whitespace normalization, unchanged already-canonical values,
  route URL absence of `%20`, invalid shape/range preservation, and mutation
  rejection.

### U3. Record the boundary

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`,
  `docs/plans/2026-06-17-coordinate-whitespace-normalization.md`
- **Requirements:** R4, R5

## Risks and Dependencies

- The change intentionally preserves numeric text rather than normalizing
  equivalent formats such as `01.0` or exponent notation.
- Live TomTom behavior and production coordinates remain outside credential-free
  validation.

## Acceptance Examples

- AE1. `" 37.77 , -122.42 "` becomes `"37.77,-122.42"`.
- AE2. `"37.77,-122.42"` remains unchanged.
- AE3. The resulting route URL contains the canonical coordinate pair and no
  `%20` around either component.
- AE4. Malformed, nonnumeric, non-finite, or out-of-range settings continue to
  raise sanitized coordinate errors.

## Verification Plan

- Run focused application and TomTom tests plus all canonical Make gates.
- Run the absolute Makefile check from an external directory.
- Reject isolated hostile mutations for stripping, canonical join, settings
  assertions, route URL assertions, guidance, and completed plan evidence.
- Audit the exact diff, artifacts, credentials, conflict markers, and intended
  paths.
