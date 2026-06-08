#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TOMTOM="$ROOT_DIR/stuff/tomtom.py"
INDEX="$ROOT_DIR/templates/index.html"

if grep -Fq "http://routes.tomtom.com" "$TOMTOM"; then
  printf '%s\n' "TomTom runtime URLs must use HTTPS." >&2
  exit 1
fi

if ! grep -Fq "https://routes.tomtom.com" "$TOMTOM"; then
  printf '%s\n' "TomTom HTTPS runtime URL is missing." >&2
  exit 1
fi

if grep -Fq "http://code.jquery.com" "$INDEX"; then
  printf '%s\n' "jQuery runtime script URL must use HTTPS." >&2
  exit 1
fi

if ! grep -Fq "https://code.jquery.com/jquery.min.js" "$INDEX"; then
  printf '%s\n' "jQuery HTTPS script URL is missing." >&2
  exit 1
fi

printf '%s\n' "morning HTTPS runtime URL baseline checks passed."
