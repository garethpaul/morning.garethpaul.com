# Security Policy

## Supported Versions

The supported security scope for `morning.garethpaul.com` is the current default branch, `master`. Older commits, tags, branches, forks, demos, and generated artifacts are not actively supported unless the repository explicitly marks them as maintained.

Project summary: Checks commute time etc via checking traffic etc.

## Reporting a Vulnerability

Please report suspected vulnerabilities through GitHub's private vulnerability reporting or by opening a draft GitHub Security Advisory for `garethpaul/morning.garethpaul.com` when that option is available. If GitHub does not show a private reporting option for this repository, contact the repository owner through GitHub and avoid posting exploit details publicly until the issue can be assessed.

Do not open a public issue that includes exploit code, secrets, personal data, or detailed reproduction steps for an unpatched vulnerability.

## What to Include

Helpful reports include:

- the affected file, endpoint, permission, dependency, or workflow
- a concise impact statement explaining what an attacker could do
- reproduction steps using test data and accounts you control
- the branch, commit SHA, platform version, device, runtime, or dependency versions used
- logs, screenshots, or proof-of-concept snippets that demonstrate impact without exposing private data

## Project Security Posture

- This repository appears to be a public sample, documentation, or utility project. The active security scope is the code and documentation on the default branch.
- Review found network clients, sockets, web APIs, or service endpoints; changes in those areas should receive security-focused review before merge.
- Review found mobile permission or privacy-sensitive data handling; changes in those areas should receive security-focused review before merge.
- Review found file, document, data, or media parsing flows; changes in those areas should receive security-focused review before merge.
- Dependency manifests detected: `requirements.txt` and `constraints.txt`.
  Preserve the direct compatibility ranges and reviewed exact CI graph. Run
  `make lint`, `make test`, `make build`, and `make check` after changing
  Python sources, TomTom route handling, local settings, templates,
  dependencies, or security docs.
- The pinned Linux workflow installs declared dependencies and runs offline
  tests without TomTom credentials, personal coordinates, local settings, or
  live route requests.
- Check target gate order should keep `make check` delegated through the named lint, test, and build targets.
- Home/work coordinates, TomTom route-service data, API keys, `.env` files, logs, and local settings overlays should stay out of git.
- Flask debug mode should remain opt-in through `FLASK_DEBUG=1` for local development only.
- Coordinate setting validation should reject malformed home/work positions without echoing raw local values.
- Coordinate range validation should reject impossible latitude/longitude values without echoing raw local values.
- Coordinate whitespace normalization should remove component-edge spaces after
  validation so accepted coordinates cannot produce a different encoded route.
- Coordinate token validation should reject Python-only forms such as numeric
  underscores and Unicode digits before constructing provider URLs.
- TomTom API key placeholder validation should reject copied template keys before live route requests.
- TomTom JSON response validation should reject malformed route responses before delay parsing.
- The TomTom Calculate Route contract should remain on `api.tomtom.com` and
  read `routes[0].summary.trafficDelayInSeconds`; legacy endpoint or response
  shapes should fail closed in offline tests.
- TomTom delay value validation should reject booleans, fractional values, and
  negative delays before route data reaches the dashboard.
- The bounded TomTom response should reject more than 1 MiB of decompressed
  parser input and close HTTP responses without exposing their content.
- TomTom transport error redaction should replace Requests transport, HTTP
  status, and response cleanup exceptions before API-key-bearing route URLs can
  reach logs.
- TomTom degraded dashboard handling should catch only stable `RuntimeError`
  and `ValueError` provider failures, render no exception detail, and leave
  unexpected programming errors visible.
- TomTom parser error redaction should raise malformed-JSON validation failures
  without retaining the provider body in a decoder exception.
- TomTom invalid encoding redaction should map invalid UTF-8 provider bytes to
  the same body-free parser error.
- TomTom integer conversion redaction should map oversized JSON integers and
  ASCII digit strings to stable errors without retaining conversion exceptions.
- Positive numeric commute settings should be enforced for distance, fuel economy, and fuel cost before rendering commute-cost output.
- Finite positive commute settings should reject `NaN` and infinity during
  loading and direct cost calculation before output reaches the dashboard.
- Settings import error preservation should suppress only an absent optional
  `settings.py`; nested dependency failures must retain their original diagnostic.
- Sanitized numeric setting errors should identify invalid fields without echoing
  raw local configuration values.
- Repository-relative Flask assets should keep checked-in templates and static
  files available when deployments start the app from a different working directory.

## Service and API Notes

For web services, APIs, sockets, or scraping workflows, prioritize reports involving authentication bypass, authorization errors, injection, server-side request forgery, unsafe deserialization, credential leakage, data exposure, or denial-of-service conditions. Use test accounts and minimal proof-of-concept traffic only.

For this commute dashboard, reports should also state whether home/work coordinates, coordinate range validation, route responses, TomTom API key placeholder validation, TomTom JSON response validation, positive numeric commute settings, sanitized numeric setting errors, repository-relative Flask assets, or precise commute patterns can be exposed.

## Dependency and Supply Chain Security

Dependency updates should come from trusted package managers and should keep manifests in sync when they exist. Do not commit credentials, private keys, tokens, generated secrets, route API keys, home/work coordinates, personal commute details, or machine-local configuration. If a vulnerability depends on a compromised package, typosquatting risk, insecure transitive dependency, or unsafe build step, include the package name, affected version, and the path through which it is used.

GitHub Actions applies `constraints.txt` to freeze the reviewed Python 3.12
resolution. This reduces resolver drift but is not artifact authentication;
the constraints file does not contain package hashes.
Flask is restricted to `>=3.1.3,<3.2`; GitHub's reviewed
`GHSA-68rp-wp8r-4726` advisory identifies 3.1.3 as the first release patched
for the session cache `Vary: Cookie` issue tracked as `CVE-2026-27205`.

## Safe Research Guidelines

Good-faith research is welcome when it stays within these boundaries:

- use only accounts, devices, data, and infrastructure that you own or have explicit permission to test
- avoid destructive actions, persistence, spam, phishing, social engineering, or denial-of-service testing
- minimize access to personal data and stop testing immediately if private data is exposed
- do not exfiltrate secrets or third-party data; report the minimum evidence needed to verify impact
- keep vulnerability details confidential until the maintainer has assessed the report

## Maintainer Response

The maintainer will review complete reports as availability allows, prioritize issues by exploitability and impact, and coordinate a fix or mitigation when the affected code is still maintained. For sample, archived, or educational repositories, the likely remediation may be documentation, dependency updates, or clearly marking unsupported code rather than a production-style patch release.
