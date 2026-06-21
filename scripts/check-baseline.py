#!/usr/bin/env python3
"""Static baseline checks for the morning dashboard."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MAKEFILE = """ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override ROOT := $(shell path='$(subst ','"'"',$(MAKEFILE_LIST))'; path=$$(printf '%s\\n' "$$path" | sed 's/^ //'); dirname -- "$$path")

.PHONY: build check clean compile lint static-check test verify

check: clean lint test build

lint: static-check

test:
\tcd "$(ROOT)" && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests

build: compile

compile:
\tcd "$(ROOT)" && python3 -c "from pathlib import Path; [compile(path.read_text(), str(path), 'exec') for path in [Path('app.py'), Path('stuff/tomtom.py'), *Path('tests').glob('*.py')]]"

static-check:
\tpython3 "$(ROOT)/scripts/check-baseline.py"

verify: check

clean:
\tfind "$(ROOT)" -type f \\( -name '*.pyc' -o -name '*.pyo' \\) -delete
\tfind "$(ROOT)" -type d -name '__pycache__' -prune -exec rm -rf {} +
"""
REQUIRED = [
    ".gitignore",
    ".github/workflows/check.yml",
    "Makefile",
    "README.md",
    "SECURITY.md",
    "VISION.md",
    "constraints.txt",
    "requirements.txt",
    "settings.py.example",
    "docs/plans/2026-06-08-morning-dashboard-baseline.md",
    "docs/plans/2026-06-08-positive-commute-settings.md",
    "docs/plans/2026-06-09-numeric-setting-error-sanitization.md",
    "docs/plans/2026-06-09-coordinate-setting-validation.md",
    "docs/plans/2026-06-09-coordinate-range-validation.md",
    "docs/plans/2026-06-09-check-target-gate-order.md",
    "docs/plans/2026-06-09-make-gate-aliases.md",
    "docs/plans/2026-06-09-tomtom-api-key-placeholder-validation.md",
    "docs/plans/2026-06-09-repository-relative-flask-assets.md",
    "docs/plans/2026-06-10-tomtom-json-response-validation.md",
    "docs/plans/2026-06-10-hosted-python-validation.md",
    "docs/plans/2026-06-10-tomtom-delay-value-validation.md",
    "docs/plans/2026-06-12-bounded-tomtom-response.md",
    "docs/plans/2026-06-12-python-dependency-constraints.md",
    "docs/plans/2026-06-13-tomtom-transport-error-redaction.md",
    "docs/plans/2026-06-13-location-independent-make.md",
    "docs/plans/2026-06-14-tomtom-parser-error-redaction.md",
    "docs/plans/2026-06-15-tomtom-invalid-encoding-redaction.md",
    "docs/plans/2026-06-16-finite-commute-settings.md",
    "docs/plans/2026-06-16-settings-import-error-preservation.md",
    "docs/plans/2026-06-17-coordinate-whitespace-normalization.md",
    "docs/plans/2026-06-21-spaced-makefile-path.md",
    "docs/plans/2026-06-21-tomtom-calculate-route.md",
    "tests/test_check_baseline.py",
    "tests/test_app.py",
    "tests/test_tomtom.py",
]
FORBIDDEN = [
    re.compile(r"urllib2"),
    re.compile(r"app\.debug\s*=\s*True"),
    re.compile(r"1e2099c7-eea9-476b-aac9-b20dc7100af1"),
]


def markdown_section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


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
    check_order_plan = (ROOT / "docs/plans/2026-06-09-check-target-gate-order.md").read_text(encoding="utf-8", errors="replace")
    api_key_plan = (ROOT / "docs/plans/2026-06-09-tomtom-api-key-placeholder-validation.md").read_text(encoding="utf-8", errors="replace")
    make_gate_plan = (ROOT / "docs/plans/2026-06-09-make-gate-aliases.md").read_text(encoding="utf-8", errors="replace")
    flask_assets_plan = (ROOT / "docs/plans/2026-06-09-repository-relative-flask-assets.md").read_text(encoding="utf-8", errors="replace")
    tomtom_json_plan = (ROOT / "docs/plans/2026-06-10-tomtom-json-response-validation.md").read_text(encoding="utf-8", errors="replace")
    hosted_validation_plan = (ROOT / "docs/plans/2026-06-10-hosted-python-validation.md").read_text(encoding="utf-8", errors="replace")
    tomtom_delay_plan = (ROOT / "docs/plans/2026-06-10-tomtom-delay-value-validation.md").read_text(encoding="utf-8", errors="replace")
    bounded_response_plan = (ROOT / "docs/plans/2026-06-12-bounded-tomtom-response.md").read_text(encoding="utf-8", errors="replace")
    constraints_plan = (ROOT / "docs/plans/2026-06-12-python-dependency-constraints.md").read_text(encoding="utf-8", errors="replace")
    transport_error_plan = (ROOT / "docs/plans/2026-06-13-tomtom-transport-error-redaction.md").read_text(encoding="utf-8", errors="replace")
    location_independent_make_plan = (ROOT / "docs/plans/2026-06-13-location-independent-make.md").read_text(encoding="utf-8", errors="replace")
    parser_error_plan = (ROOT / "docs/plans/2026-06-14-tomtom-parser-error-redaction.md").read_text(encoding="utf-8", errors="replace")
    invalid_encoding_plan = (ROOT / "docs/plans/2026-06-15-tomtom-invalid-encoding-redaction.md").read_text(encoding="utf-8", errors="replace")
    finite_settings_plan = (ROOT / "docs/plans/2026-06-16-finite-commute-settings.md").read_text(encoding="utf-8", errors="replace")
    settings_import_plan = (ROOT / "docs/plans/2026-06-16-settings-import-error-preservation.md").read_text(encoding="utf-8", errors="replace")
    coordinate_normalization_plan = (ROOT / "docs/plans/2026-06-17-coordinate-whitespace-normalization.md").read_text(encoding="utf-8", errors="replace")
    spaced_makefile_plan = (ROOT / "docs/plans/2026-06-21-spaced-makefile-path.md").read_text(encoding="utf-8", errors="replace")
    calculate_route_plan = (ROOT / "docs/plans/2026-06-21-tomtom-calculate-route.md").read_text(encoding="utf-8", errors="replace")
    constraints = (ROOT / "constraints.txt").read_text(encoding="utf-8", errors="replace")
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8", errors="replace")
    workflow = (ROOT / ".github/workflows/check.yml").read_text(encoding="utf-8", errors="replace")
    tomtom_source = (ROOT / "stuff" / "tomtom.py").read_text(encoding="utf-8", errors="replace")

    expected_requirements = """Flask>=3.1.3,<3.2
requests>=2.31,<3
"""
    expected_constraints = """# Reviewed CI resolution for Python 3.12.
blinker==1.9.0
certifi==2026.5.20
charset-normalizer==3.4.7
click==8.4.1
Flask==3.1.3
idna==3.18
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
requests==2.34.2
urllib3==2.7.0
Werkzeug==3.1.8
"""
    constrained_install = (
        "python -m pip install --requirement requirements.txt "
        "--constraint constraints.txt"
    )
    dependency_cache = """          cache-dependency-path: |
            requirements.txt
            constraints.txt"""

    if "status: completed" not in hosted_validation_plan or "make check" not in hosted_validation_plan:
        failures.append("hosted Python validation plan must be marked completed")
    if not all(value in workflow for value in [
        "permissions:\n  contents: read",
        "cancel-in-progress: true",
        "runs-on: ubuntu-24.04",
        "timeout-minutes: 10",
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        "persist-credentials: false",
        "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405",
        'python-version: "3.12"',
        "python -m pip check",
        "run: make check",
    ]) or workflow.count(dependency_cache) != 1 or workflow.count(constrained_install) != 1:
        failures.append("Check workflow must stay pinned, read-only, bounded, and dependency-aware")
    if workflow.count("uses: actions/checkout@") != 1 or workflow.count("persist-credentials: false") != 1:
        failures.append("Check workflow must contain one credential-free checkout step")
    if requirements != expected_requirements:
        failures.append("requirements.txt must preserve the reviewed direct compatibility ranges")
    if constraints != expected_constraints:
        failures.append("constraints.txt must match the reviewed Python 3.12 graph exactly")
    if not all("constraints.txt" in text for text in [readme, security, changes]):
        failures.append("docs must describe the reviewed dependency constraints")
    if "do not authenticate" not in readme.lower() or "not artifact authentication" not in security.lower():
        failures.append("docs must describe the constraints artifact-authentication boundary")
    constraints_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", constraints_plan)
    constraints_work = markdown_section(constraints_plan, "Work Completed")
    constraints_verification = markdown_section(constraints_plan, "Verification Completed")
    if constraints_status != ["completed"] or not constraints_work:
        failures.append("dependency constraints plan must record one completed status and completed work")
    if not constraints_verification or re.search(
        r"(?i)\b(?:pending|todo|tbd|not run|will be recorded)\b",
        constraints_verification,
    ):
        failures.append("dependency constraints plan must record finished verification")
    elif not all(evidence in constraints_verification for evidence in [
        "Official PyPI metadata",
        "GHSA-68rp-wp8r-4726",
        "Python 3.10, 3.12, and 3.14",
        "12-package graph",
        "python -m pip check",
        "pip-audit -r constraints.txt --no-deps",
        "no known vulnerabilities",
        "make check",
        "hostile mutations",
        "git diff --check",
        "1adf9d43e3dcea2fb211ea3318d56bc90c610ac5",
        "27437919847",
        "27437931925",
        "27437930574",
        "all five exact-head checks successful",
        "zero open PR-scoped",
    ]):
        failures.append("dependency constraints plan must preserve exact local verification evidence")
    test_tomtom = (ROOT / "tests" / "test_tomtom.py").read_text(encoding="utf-8", errors="replace")

    if makefile != EXPECTED_MAKEFILE:
        failures.append("Makefile must exactly preserve rooted lint, test, build, check, verify, and clean gates")
    if not all(value in spaced_makefile_plan for value in [
        "status: completed",
        "spaces, brackets, and an apostrophe",
        "MAKEFILE_LIST",
        "all eight Make aliases",
    ]):
        failures.append("spaced Makefile path plan must preserve completed hostile-path and override verification")
    if "make -f /path/to/morning.garethpaul.com/Makefile check" not in readme:
        failures.append("README must document location-independent Makefile invocation")
    if not all(value in location_independent_make_plan for value in [
        "status: completed",
        "root and external-directory",
        "eight isolated hostile mutations",
    ]):
        failures.append("location-independent Make plan must record completed root, external, and mutation verification")

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
    if not all(value in app_source for value in [
        "import math",
        "def _finite_positive(number: float, name: str) -> float:",
        "if not math.isfinite(number) or number <= 0:",
        "return _finite_positive(_to_float(value, name), name)",
        '_finite_positive(self.work_miles, "work_miles")',
        '_finite_positive(self.miles_per_gallon, "miles_per_gallon")',
        '_finite_positive(self.cost_per_gallon, "cost_per_gallon")',
    ]):
        failures.append("commute numeric settings and direct cost calculation must require finite positive values")
    if not all(value in test_app for value in [
        "test_load_settings_rejects_non_finite_numeric_settings",
        "test_cost_per_day_rejects_non_finite_direct_values",
        "math.nan, math.inf, -math.inf",
    ]):
        failures.append("tests must cover non-finite loaded and direct commute numeric values")
    if not all("finite positive commute settings" in text.lower() for text in [readme, vision, security]):
        failures.append("docs must mention finite positive commute settings")
    if "finite positive commute settings" not in changes.lower():
        failures.append("CHANGES must record finite positive commute settings validation")
    if not all(value in finite_settings_plan for value in [
        "Status: completed",
        "all 22 offline tests",
        "All four Make gates passed",
        "external directory",
        "Eight isolated hostile mutations were rejected",
    ]) or re.search(
        r"(?i)\b(?:pending|todo|tbd|not run)\b",
        markdown_section(finite_settings_plan, "Verification Completed"),
    ):
        failures.append("finite commute settings plan must record completed verification")
    optional_settings_start = app_source.find("def _load_optional_settings_module():")
    optional_settings_end = app_source.find("\n\ndef _module_value", optional_settings_start)
    optional_settings_source = app_source[optional_settings_start:optional_settings_end]
    if not all(value in optional_settings_source for value in [
        'return importlib.import_module("settings")',
        "except ModuleNotFoundError as error:",
        'if error.name != "settings":',
        "raise",
        "return None",
    ]):
        failures.append("optional settings import must preserve nested ModuleNotFoundError failures")
    if not all(value in test_app for value in [
        "test_optional_settings_module_allows_top_level_absence",
        "test_optional_settings_module_preserves_nested_import_failure",
        'name="settings"',
        'name="private_settings_dependency"',
        "self.assertIs(raised.exception, missing_dependency)",
    ]):
        failures.append("tests must distinguish absent settings from nested import failures")
    if not all("settings import error preservation" in text.lower() for text in [readme, vision, security, changes]):
        failures.append("docs must describe settings import error preservation")
    if not all(value in settings_import_plan for value in [
        "Status: completed",
        "all 24 offline tests",
        "All four Make gates passed",
        "external directory",
        "Seven isolated hostile mutations were rejected",
        "git diff --check",
    ]) or re.search(
        r"(?i)\b(?:pending|todo|tbd|not run)\b",
        markdown_section(settings_import_plan, "Verification Completed"),
    ):
        failures.append("settings import error preservation plan must record completed verification")
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
    if not all(token in app_source for token in [
        'COORDINATE_COMPONENT = re.compile(',
        "re.ASCII",
        "normalized_parts = [part.strip() for part in parts]",
        "COORDINATE_COMPONENT.fullmatch(part)",
        "latitude = float(normalized_parts[0])",
        "longitude = float(normalized_parts[1])",
        'return ",".join(normalized_parts)',
    ]):
        failures.append("validated commute coordinates must be returned without component-edge whitespace")
    if not all(token in test_app for token in [
        "test_load_settings_rejects_noncanonical_coordinate_tokens",
        '"3_7.77,-122.42"',
        '"٣٧.٧٧,-122.42"',
    ]):
        failures.append("tests must reject noncanonical ASCII and Unicode coordinate tokens")
    if not all(token in test_app for token in [
        "test_load_settings_normalizes_coordinate_whitespace_for_route_urls",
        'self.assertEqual(settings.home_pos, "37.77,-122.42")',
        'self.assertEqual(settings.work_pos, "37.79,-122.40")',
        'self.assertNotIn("%20", url)',
    ]):
        failures.append("tests must cover coordinate normalization through TomTom route construction")
    if not all("coordinate whitespace normalization" in text.lower() for text in [readme, vision, security, changes]):
        failures.append("project guidance must document coordinate whitespace normalization")
    if not all(token in coordinate_normalization_plan for token in [
        "status: completed",
        "All 25 offline tests passed",
        "All four Make gates passed",
        "external directory",
        "Seven isolated hostile mutations were rejected",
        "No live TomTom request was made",
    ]) or re.search(
        r"(?i)\b(?:pending|todo|tbd|not run)\b",
        markdown_section(coordinate_normalization_plan, "Verification Completed"),
    ):
        failures.append("coordinate whitespace normalization plan must record completed verification")
    if "status: completed" not in check_order_plan:
        failures.append("check target gate order plan must be marked completed")
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
    if not all("check target gate order" in text.lower() for text in [readme, vision, security]):
        failures.append("docs must mention check target gate order")
    if "make lint" not in changes or "make test" not in changes or "make build" not in changes or "make check" not in changes:
        failures.append("CHANGES must record Make gate aliases")
    if "check target gate order" not in changes.lower():
        failures.append("CHANGES must record check target gate order")
    if "status: completed" not in make_gate_plan:
        failures.append("Make gate alias plan must be marked completed")
    if "BASE_DIR = Path(__file__).resolve().parent" not in app_source:
        failures.append("Flask app must derive asset paths from the repository directory")
    if "static_folder=str(BASE_DIR / \"static\")" not in app_source or "template_folder=str(BASE_DIR / \"templates\")" not in app_source:
        failures.append("Flask app must use repository-relative static and template folders")
    if "test_create_app_serves_static_assets_when_cwd_changes" not in test_app:
        failures.append("tests must cover repository-relative Flask static assets")
    if not all("repository-relative flask assets" in text.lower() for text in [readme, vision, security]):
        failures.append("docs must mention repository-relative Flask assets")
    if "repository-relative flask assets" not in changes.lower():
        failures.append("CHANGES must record repository-relative Flask assets")
    if "status: completed" not in flask_assets_plan:
        failures.append("repository-relative Flask assets plan must be marked completed")
    if "json.JSONDecodeError" not in tomtom_source or "TomTom response must be valid JSON" not in tomtom_source:
        failures.append("TomTom response parsing must reject malformed JSON with a stable error")
    if "test_parse_delay_seconds_rejects_invalid_json" not in test_tomtom:
        failures.append("tests must cover TomTom JSON response validation")
    if not all("tomtom json response validation" in text.lower() for text in [readme, vision, security]):
        failures.append("docs must mention TomTom JSON response validation")
    if "tomtom json response validation" not in changes.lower():
        failures.append("CHANGES must record TomTom JSON response validation")
    if "status: completed" not in tomtom_json_plan:
        failures.append("TomTom JSON response validation plan must be marked completed")
    if not all(value in tomtom_source for value in [
        "https://api.tomtom.com/routing/1/calculateRoute/",
        "?key={api_key}&traffic=true&routeType=fastest",
        'payload["routes"][0]["summary"]["trafficDelayInSeconds"]',
    ]) or any(value in tomtom_source for value in [
        "routes.tomtom.com",
        "totalDelaySeconds",
    ]):
        failures.append("TomTom routing must use the current Calculate Route request and response contract")
    if not all(value in test_tomtom for value in [
        "test_route_url_uses_current_calculate_route_contract",
        "test_parse_delay_seconds_rejects_missing_or_malformed_route_data",
        "https://api.tomtom.com/routing/1/calculateRoute/1,2:3,4/json",
        '"route": {"summary": {"totalDelaySeconds": 42}}',
        "self.assertNotIn(\"Referer\", calls[0][1])",
    ]):
        failures.append("tests must cover the current TomTom contract and reject legacy or malformed responses")
    if not all("TomTom Calculate Route contract" in text for text in [readme, vision, security, changes]):
        failures.append("docs must describe the current TomTom Calculate Route contract")
    if not all(value in readme for value in [
        "historical project name",
        "No deployment configuration is included",
        "TOMTOM_API_KEY",
    ]):
        failures.append("README must document deployment status and required TomTom configuration")
    if "status: completed" not in calculate_route_plan:
        failures.append("TomTom Calculate Route plan must be marked completed")
    if "isinstance(value, bool)" not in tomtom_source or "if delay < 0" not in tomtom_source or "normalized.isascii()" not in tomtom_source:
        failures.append("TomTom delay parsing must accept only non-negative integers or ASCII digit strings")
    if "test_parse_delay_seconds_rejects_invalid_delay_values" not in test_tomtom or "True, False, -1, 1.5" not in test_tomtom:
        failures.append("tests must cover invalid TomTom delay value types and ranges")
    if not all("tomtom delay value validation" in text.lower() for text in [readme, vision, security]):
        failures.append("docs must mention TomTom delay value validation")
    if "tomtom delay value validation" not in changes.lower():
        failures.append("CHANGES must record TomTom delay value validation")
    tomtom_delay_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", tomtom_delay_plan)
    tomtom_delay_work = markdown_section(tomtom_delay_plan, "Work Completed")
    tomtom_delay_verification = markdown_section(
        tomtom_delay_plan, "Verification Completed"
    )
    if tomtom_delay_status != ["completed"] or not tomtom_delay_work:
        failures.append("TomTom delay value validation plan must record one completed status and completed work")
    if not tomtom_delay_verification or re.search(
        r"(?i)\b(?:pending|todo|tbd|not run)\b", tomtom_delay_verification
    ):
        failures.append("TomTom delay value validation plan must record completed verification")
    for evidence in [
        "make check",
        "make lint",
        "make test",
        "make build",
        "python3 -m py_compile scripts/check-baseline.py",
        "git diff --check",
        "27397385338",
        "27397386885",
        "bffbd99b97eb8868ee9e618ecf4be2132ed33a64",
        "isinstance(value, bool)",
        "normalized.isascii()",
        "if delay < 0",
        "test_parse_delay_seconds_accepts_non_negative_integers",
        "test_parse_delay_seconds_rejects_invalid_delay_values",
    ]:
        if evidence not in tomtom_delay_verification:
            failures.append(f"TomTom delay verification must record {evidence}")
    if not all(value in tomtom_source for value in [
        "MAXIMUM_TOMTOM_RESPONSE_BYTES = 1024 * 1024",
        "stream=True",
        "response.iter_content",
        "remaining = MAXIMUM_TOMTOM_RESPONSE_BYTES + 1 - len(body)",
        "body.extend(chunk[:remaining])",
        "if len(body) > MAXIMUM_TOMTOM_RESPONSE_BYTES",
        "TomTom response exceeds 1 MiB limit",
        "finally:\n        if response is not None:",
        "try:\n                response.close()",
        "except Exception:\n                request_failed = True",
    ]):
        failures.append("TomTom responses must be streamed, bounded, and closed before parsing")
    if not all(value in test_tomtom for value in [
        "test_traffic_delay_seconds_rejects_oversized_response_and_closes_it",
        "test_traffic_delay_seconds_closes_response_when_status_check_fails",
        "self.assertTrue(response.closed)",
    ]):
        failures.append("tests must cover bounded and closed TomTom responses")
    if not all("bounded TomTom response" in text for text in [readme, vision, security, changes]):
        failures.append("docs must describe the bounded TomTom response")
    if "status: completed" not in bounded_response_plan or "hostile mutations" not in bounded_response_plan:
        failures.append("bounded TomTom response plan must record completed verification")
    if not all(value in tomtom_source for value in [
        "except requests.RequestException:",
        "request_failed = True",
        'raise RuntimeError("TomTom request failed")',
    ]):
        failures.append("TomTom request failures must use a stable credential-redacted error boundary")
    if not all(value in test_tomtom for value in [
        "test_traffic_delay_seconds_redacts_transport_error_url",
        "test_traffic_delay_seconds_redacts_response_close_errors",
        "requests.Timeout",
        "requests.HTTPError",
        "self.assertIsNone(raised.exception.__context__)",
        "self.assertNotIn(secret, str(raised.exception))",
    ]):
        failures.append("tests must prove TomTom transport errors do not retain or expose the API key")
    if not all("TomTom transport error redaction" in text for text in [readme, vision, security, changes]):
        failures.append("docs must describe TomTom transport error redaction")
    if "status: completed" not in transport_error_plan or "hostile mutations" not in transport_error_plan:
        failures.append("TomTom transport error redaction plan must record completed verification")
    if not all(value in tomtom_source for value in [
        "invalid_json = False",
        "except (json.JSONDecodeError, UnicodeDecodeError):",
        "invalid_json = True",
        "if invalid_json:",
        'raise ValueError("TomTom response must be valid JSON")',
    ]):
        failures.append("TomTom parser failures must use a response-body-redacted error boundary")
    if not all(value in test_tomtom for value in [
        "test_parse_delay_seconds_redacts_invalid_json_body",
        "self.assertIsNone(raised.exception.__cause__)",
        "self.assertIsNone(raised.exception.__context__)",
        "self.assertNotIn(secret, str(raised.exception))",
    ]):
        failures.append("tests must prove malformed TomTom response bodies are not retained by parser errors")
    if not all("TomTom parser error redaction" in text for text in [readme, vision, security, changes]):
        failures.append("docs must describe TomTom parser error redaction")
    if "status: completed" not in parser_error_plan or "hostile mutations" not in parser_error_plan:
        failures.append("TomTom parser error redaction plan must record completed verification")
    if not all(value in test_tomtom for value in [
        "test_parse_delay_seconds_redacts_invalid_utf8_body",
        "private-provider-byte-token",
        "b'\\xff",
        "self.assertIsNone(raised.exception.__cause__)",
        "self.assertIsNone(raised.exception.__context__)",
        "self.assertNotIn(secret, str(raised.exception))",
    ]):
        failures.append("tests must prove invalid UTF-8 TomTom bodies use the redacted parser boundary")
    if not all("TomTom invalid encoding redaction" in text for text in [readme, vision, security, changes]):
        failures.append("docs must describe TomTom invalid encoding redaction")
    if not all(value in invalid_encoding_plan for value in [
        "status: completed",
        "All four Make gates passed",
        "external-directory Make gate",
        "Six isolated hostile mutations were rejected",
        "git diff --check",
    ]) or re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", markdown_section(invalid_encoding_plan, "Verification Completed")):
        failures.append("TomTom invalid encoding plan must record completed verification")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("morning dashboard baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
