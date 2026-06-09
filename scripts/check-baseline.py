#!/usr/bin/env python3
"""Static baseline checks for the morning dashboard."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ".gitignore",
    "Makefile",
    "README.md",
    "SECURITY.md",
    "VISION.md",
    "requirements.txt",
    "settings.py.example",
    "docs/plans/2026-06-08-morning-dashboard-baseline.md",
    "docs/plans/2026-06-08-positive-commute-settings.md",
    "docs/plans/2026-06-09-numeric-setting-error-sanitization.md",
    "docs/plans/2026-06-09-coordinate-setting-validation.md",
    "docs/plans/2026-06-09-coordinate-range-validation.md",
    "docs/plans/2026-06-09-make-gate-aliases.md",
    "docs/plans/2026-06-09-tomtom-api-key-placeholder-validation.md",
    "tests/test_app.py",
    "tests/test_tomtom.py",
]
FORBIDDEN = [
    re.compile(r"urllib2"),
    re.compile(r"app\.debug\s*=\s*True"),
    re.compile(r"1e2099c7-eea9-476b-aac9-b20dc7100af1"),
]


def main() -> int:
    failures = []
    for relative_path in REQUIRED:
        if not (ROOT / relative_path).is_file():
            failures.append(f"required file missing: {relative_path}")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8", errors="replace")
    for expected in ["settings.py", ".env", "__pycache__/", "*.pyc"]:
        if expected not in gitignore:
            failures.append(f".gitignore must include {expected}")

    for path in [ROOT / "app.py", ROOT / "stuff" / "tomtom.py"]:
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in FORBIDDEN:
            if pattern.search(text):
                failures.append(f"forbidden legacy pattern {pattern.pattern} found in {path.relative_to(ROOT)}")

    settings_example = (ROOT / "settings.py.example").read_text(encoding="utf-8", errors="replace")
    if re.search(r'(home_pos|work_pos)\s*=\s*"[0-9.-]+,[0-9.-]+"', settings_example):
        failures.append("settings.py.example must use non-personal coordinate placeholders")

    template = (ROOT / "templates" / "index.html").read_text(encoding="utf-8", errors="replace")
    if "code.jquery.com" in template:
        failures.append("template must not depend on remote jQuery for simple click handlers")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.suffix in {".pyc", ".pyo"}:
            failures.append(f"compiled Python artifact found: {path.relative_to(ROOT)}")

    app_source = (ROOT / "app.py").read_text(encoding="utf-8", errors="replace")
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8", errors="replace")
    test_app = (ROOT / "tests/test_app.py").read_text(encoding="utf-8", errors="replace")
    readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
    vision = (ROOT / "VISION.md").read_text(encoding="utf-8", errors="replace")
    security = (ROOT / "SECURITY.md").read_text(encoding="utf-8", errors="replace")
    changes = (ROOT / "CHANGES.md").read_text(encoding="utf-8", errors="replace")
    settings_plan = (ROOT / "docs/plans/2026-06-08-positive-commute-settings.md").read_text(encoding="utf-8", errors="replace")
    numeric_error_plan = (ROOT / "docs/plans/2026-06-09-numeric-setting-error-sanitization.md").read_text(encoding="utf-8", errors="replace")
    coordinate_plan = (ROOT / "docs/plans/2026-06-09-coordinate-setting-validation.md").read_text(encoding="utf-8", errors="replace")
    coordinate_range_plan = (ROOT / "docs/plans/2026-06-09-coordinate-range-validation.md").read_text(encoding="utf-8", errors="replace")
    api_key_plan = (ROOT / "docs/plans/2026-06-09-tomtom-api-key-placeholder-validation.md").read_text(encoding="utf-8", errors="replace")
    make_gate_plan = (ROOT / "docs/plans/2026-06-09-make-gate-aliases.md").read_text(encoding="utf-8", errors="replace")

    for target in ["lint: static-check", "test:", "build: compile", "compile:", "static-check:", "verify: check", "check: clean test compile static-check"]:
        if target not in makefile:
            failures.append(f"Makefile must expose target: {target}")

    if "_positive_float" not in app_source or "must be greater than zero" not in app_source:
        failures.append("app settings must reject non-positive commute numeric values")
    if "test_load_settings_rejects_non_positive_numeric_settings" not in test_app:
        failures.append("tests must cover non-positive commute numeric values")
    if not all("positive numeric" in text.lower() for text in [readme, vision, security]):
        failures.append("docs must mention positive numeric commute settings")
    if "positive numeric" not in changes.lower():
        failures.append("CHANGES must record positive numeric commute settings validation")
    if "status: completed" not in settings_plan:
        failures.append("positive commute settings plan must be marked completed")
    if "raise ValueError(f\"{name} must be numeric\") from None" not in app_source:
        failures.append("numeric commute settings must not expose raw conversion values")
    if "test_load_settings_rejects_non_numeric_settings_without_raw_cause" not in test_app:
        failures.append("tests must cover sanitized non-numeric commute setting errors")
    if not all("sanitized numeric setting errors" in text.lower() for text in [readme, vision, security]):
        failures.append("docs must mention sanitized numeric setting errors")
    if "sanitized numeric setting errors" not in changes.lower():
        failures.append("CHANGES must record sanitized numeric setting errors")
    if "status: completed" not in numeric_error_plan:
        failures.append("numeric setting error sanitization plan must be marked completed")
    if "_coordinate_pair" not in app_source or "numeric coordinate pair" not in app_source:
        failures.append("app settings must validate coordinate pairs")
    if "test_load_settings_rejects_invalid_coordinates_without_raw_value" not in test_app:
        failures.append("tests must cover sanitized coordinate setting validation")
    if not all("coordinate setting validation" in text.lower() for text in [readme, vision, security]):
        failures.append("docs must mention coordinate setting validation")
    if "coordinate setting validation" not in changes.lower():
        failures.append("CHANGES must record coordinate setting validation")
    if "status: completed" not in coordinate_plan:
        failures.append("coordinate setting validation plan must be marked completed")
    if "-90 <= latitude <= 90" not in app_source or "-180 <= longitude <= 180" not in app_source:
        failures.append("app settings must validate coordinate latitude/longitude ranges")
    if "test_load_settings_rejects_out_of_range_coordinates_without_raw_value" not in test_app:
        failures.append("tests must cover sanitized coordinate range validation")
    if not all("coordinate range validation" in text.lower() for text in [readme, vision, security]):
        failures.append("docs must mention coordinate range validation")
    if "coordinate range validation" not in changes.lower():
        failures.append("CHANGES must record coordinate range validation")
    if "status: completed" not in coordinate_range_plan:
        failures.append("coordinate range validation plan must be marked completed")
    if "_configured_api_key" not in app_source or "YOUR_TOMTOM_API_KEY" not in app_source:
        failures.append("app settings must reject placeholder TomTom API keys")
    if "test_load_settings_rejects_placeholder_tomtom_api_key" not in test_app:
        failures.append("tests must cover TomTom API key placeholder validation")
    if not all("tomtom api key placeholder validation" in text.lower() for text in [readme, vision, security]):
        failures.append("docs must mention TomTom API key placeholder validation")
    if "tomtom api key placeholder validation" not in changes.lower():
        failures.append("CHANGES must record TomTom API key placeholder validation")
    if "status: completed" not in api_key_plan:
        failures.append("TomTom API key placeholder validation plan must be marked completed")
    if not all("make lint" in text and "make test" in text and "make build" in text and "make check" in text for text in [readme, vision, security]):
        failures.append("docs must mention lint, test, build, and check gate targets")
    if "make lint" not in changes or "make test" not in changes or "make build" not in changes or "make check" not in changes:
        failures.append("CHANGES must record Make gate aliases")
    if "status: completed" not in make_gate_plan:
        failures.append("Make gate alias plan must be marked completed")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("morning dashboard baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
