#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
APP="$ROOT_DIR/app.py"

if grep -Fq "app.debug = True" "$APP"; then
  printf '%s\n' "app.py must not enable Flask debug mode by default." >&2
  exit 1
fi

if ! grep -Fq "debug=debug_enabled()" "$APP"; then
  printf '%s\n' "app.run must use the explicit debug helper." >&2
  exit 1
fi

if ! grep -Fq "MORNING_DEBUG" "$APP"; then
  printf '%s\n' "app.py must expose an explicit local debug flag." >&2
  exit 1
fi

printf '%s\n' "morning debug baseline checks passed."
