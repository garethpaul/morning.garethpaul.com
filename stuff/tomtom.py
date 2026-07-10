"""TomTom route helpers for the morning commute dashboard."""

from __future__ import annotations

import json
from typing import Callable
from urllib.parse import quote

import requests


ROUTE_TEMPLATE = (
    "https://api.tomtom.com/routing/1/calculateRoute/"
    "{start}:{end}/json?key={api_key}&traffic=true&routeType=fastest"
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
            headers={"User-Agent": USER_AGENT},
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
        except (ValueError, RecursionError):
            invalid_json = True
        if invalid_json:
            raise ValueError("TomTom response must be valid JSON")
    missing_route_data = False
    try:
        value = payload["routes"][0]["summary"]["trafficDelayInSeconds"]
    except (IndexError, KeyError, TypeError):
        missing_route_data = True
    if missing_route_data:
        raise ValueError(
            "TomTom response missing routes[0].summary.trafficDelayInSeconds"
        )

    if isinstance(value, bool):
        raise ValueError("TomTom trafficDelayInSeconds must be a non-negative integer")
    if isinstance(value, int):
        if value < 0:
            raise ValueError("TomTom trafficDelayInSeconds must be a non-negative integer")
        if value > 31536000:
            raise ValueError("TomTom trafficDelayInSeconds must be a non-negative integer")
        delay = value
    elif isinstance(value, str):
        normalized = value.strip()
        if not normalized.isascii() or not normalized.isdigit():
            raise ValueError("TomTom trafficDelayInSeconds must be a non-negative integer")
        invalid_delay = False
        try:
            delay = int(normalized)
        except ValueError:
            invalid_delay = True
        if invalid_delay:
            raise ValueError("TomTom trafficDelayInSeconds must be a non-negative integer")
        if delay > 31536000:
            raise ValueError("TomTom trafficDelayInSeconds must be a non-negative integer")
    else:
        raise ValueError("TomTom trafficDelayInSeconds must be a non-negative integer")

    if delay < 0:
        raise ValueError("TomTom trafficDelayInSeconds must be a non-negative integer")
    return delay
