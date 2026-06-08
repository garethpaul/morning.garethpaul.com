# Issue 1 HTTPS Runtime URLs

## Issue

`garethpaul/morning.garethpaul.com#1` reports that TomTom runtime route
requests use plain HTTP.

## Plan

- Move TomTom route URLs from HTTP to HTTPS.
- Move the TomTom referer header to HTTPS.
- Move the page's jQuery script URL to HTTPS.
- Add a source-level baseline check for these runtime URLs.

## Verification

- `scripts/check-baseline.sh`
- `rg -n "http://routes\\.tomtom\\.com|https://routes\\.tomtom\\.com|http://code\\.jquery\\.com|https://code\\.jquery\\.com" stuff/tomtom.py templates/index.html scripts/check-baseline.sh`
- `git diff --check`
- `curl -I -L --max-time 15 https://routes.tomtom.com/` *(blocked locally: host does not resolve)*
