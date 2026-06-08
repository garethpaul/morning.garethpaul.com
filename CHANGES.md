# Changes

## 2026-06-08

- Added `make check` with Python compilation and static baseline checks.
- Made commute-cost calculation tolerate placeholder local settings.
- Moved committed settings placeholders to `settings.py.example` while allowing local `settings.py` at runtime.
- Fixed the `/home` route to request home traffic instead of the misspelled route key.
- Disabled Flask debug mode by default and allowed opt-in via `FLASK_DEBUG=1`.
- Switched TomTom and jQuery URLs to HTTPS.
