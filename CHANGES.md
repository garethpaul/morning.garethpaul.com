# Changes

## 2026-06-08

- Added `make check` with Python compilation and static baseline checks.
- Added offline tests for settings loading, Flask route rendering, TomTom URL construction, response parsing, and injected HTTP calls.
- Added `requirements.txt` for Flask and requests.
- Made commute-cost calculation load from explicit environment or ignored local settings.
- Moved committed settings placeholders to `settings.py.example` while allowing local `settings.py` at runtime.
- Fixed the `/home` route to request home traffic instead of the misspelled route key.
- Disabled Flask debug mode by default and allowed opt-in via `FLASK_DEBUG=1`.
- Kept TomTom route calls on HTTPS and removed the remote jQuery dependency.
