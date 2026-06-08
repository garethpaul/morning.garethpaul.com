#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TOMTOM="$ROOT_DIR/stuff/tomtom.py"

if grep -Fq "urllib2.urlopen(request)" "$TOMTOM"; then
  printf '%s\n' "TomTom request must not call urlopen without a timeout." >&2
  exit 1
fi

grep -Fq "URL_TIMEOUT_SECONDS = 10" "$TOMTOM"
grep -Fq "urllib2.urlopen(request, timeout=URL_TIMEOUT_SECONDS)" "$TOMTOM"

printf '%s\n' "morning TomTom timeout baseline checks passed."
