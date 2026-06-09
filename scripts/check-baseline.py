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
    test_app = (ROOT / "tests/test_app.py").read_text(encoding="utf-8", errors="replace")
    readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
    vision = (ROOT / "VISION.md").read_text(encoding="utf-8", errors="replace")
    security = (ROOT / "SECURITY.md").read_text(encoding="utf-8", errors="replace")
    changes = (ROOT / "CHANGES.md").read_text(encoding="utf-8", errors="replace")
    settings_plan = (ROOT / "docs/plans/2026-06-08-positive-commute-settings.md").read_text(encoding="utf-8", errors="replace")

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

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("morning dashboard baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
