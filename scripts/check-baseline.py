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

    template = (ROOT / "templates" / "index.html").read_text(encoding="utf-8", errors="replace")
    if "code.jquery.com" in template:
        failures.append("template must not depend on remote jQuery for simple click handlers")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.suffix in {".pyc", ".pyo"}:
            failures.append(f"compiled Python artifact found: {path.relative_to(ROOT)}")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("morning dashboard baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
