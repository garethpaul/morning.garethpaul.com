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
    response = http_get(
        route_url(where, settings),
        headers={
            "User-Agent": USER_AGENT,
            "Referer": "https://routes.tomtom.com/",
        },
        timeout=10,
    )
    response.raise_for_status()
    return parse_delay_seconds(response.text)


def parse_delay_seconds(payload) -> int:
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError as error:
            raise ValueError("TomTom response must be valid JSON") from error
    try:
        return int(payload["route"]["summary"]["totalDelaySeconds"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("TomTom response missing route.summary.totalDelaySeconds") from error
