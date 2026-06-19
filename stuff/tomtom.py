"""TomTom route helpers for the morning commute dashboard."""

from __future__ import annotations

import json
from typing import Callable
from urllib.parse import quote

import requests


ROUTE_TEMPLATE = (
    "https://routes.tomtom.com/lbs/services/route/1/"
    "{start}:{end}/Quickest/json/{api_key};"
    "language=en;avoidTraffic=true;includeTraffic=true;day=today;"
    "time=now;iqRoutes=2;trafficModelId=1358732719560;map=basic"
)
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) "
    "AppleWebKit/537.27 (KHTML, like Gecko) Chrome/26.0.1386.0 Safari/537.27"
)
MAXIMUM_TOMTOM_RESPONSE_BYTES = 1024 * 1024
TOMTOM_RESPONSE_CHUNK_BYTES = 64 * 1024


def route_url(where: str, settings) -> str:
    if where == "work":
        start, end = settings.home_pos, settings.work_pos
    elif where == "home":
        start, end = settings.work_pos, settings.home_pos
    else:
        raise ValueError("where must be 'home' or 'work'")

    return ROUTE_TEMPLATE.format(
        start=quote(start, safe=","),
        end=quote(end, safe=","),
        api_key=quote(settings.tomtom_api_key, safe=""),
    )


def traffic_delay_seconds(where: str, settings, http_get: Callable = requests.get) -> int:
    response = None
    request_failed = False
    delay = None
    try:
        response = http_get(
            route_url(where, settings),
            headers={
                "User-Agent": USER_AGENT,
                "Referer": "https://routes.tomtom.com/",
            },
            timeout=10,
            stream=True,
        )
        response.raise_for_status()
        delay = parse_delay_seconds(read_tomtom_response(response))
    except requests.RequestException:
        request_failed = True
    finally:
        if response is not None:
            try:
                response.close()
            except Exception:
                request_failed = True

    if request_failed:
        raise RuntimeError("TomTom request failed")
    return delay


def read_tomtom_response(response) -> bytes:
    body = bytearray()
    for chunk in response.iter_content(chunk_size=TOMTOM_RESPONSE_CHUNK_BYTES):
        if not chunk:
            continue
        remaining = MAXIMUM_TOMTOM_RESPONSE_BYTES + 1 - len(body)
        body.extend(chunk[:remaining])
        if len(body) > MAXIMUM_TOMTOM_RESPONSE_BYTES:
            raise ValueError("TomTom response exceeds 1 MiB limit")
    return bytes(body)


def parse_delay_seconds(payload) -> int:
    if isinstance(payload, (str, bytes, bytearray)):
        invalid_json = False
        try:
            payload = json.loads(payload)
        except (json.JSONDecodeError, UnicodeDecodeError):
            invalid_json = True
        if invalid_json:
            raise ValueError("TomTom response must be valid JSON")
    try:
        value = payload["route"]["summary"]["totalDelaySeconds"]
    except (KeyError, TypeError) as error:
        raise ValueError("TomTom response missing route.summary.totalDelaySeconds") from error

    if isinstance(value, bool):
        raise ValueError("TomTom totalDelaySeconds must be a non-negative integer")
    if isinstance(value, int):
        delay = value
    elif isinstance(value, str):
        normalized = value.strip()
        if not normalized.isascii() or not normalized.isdigit():
            raise ValueError("TomTom totalDelaySeconds must be a non-negative integer")
        try:
            delay = int(normalized)
        except ValueError as error:
            raise ValueError("TomTom totalDelaySeconds must be a non-negative integer") from error
    else:
        raise ValueError("TomTom totalDelaySeconds must be a non-negative integer")

    if delay < 0:
        raise ValueError("TomTom totalDelaySeconds must be a non-negative integer")
    return delay
