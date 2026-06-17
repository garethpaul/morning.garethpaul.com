"""Flask entry point for the morning commute dashboard."""

from __future__ import annotations

from dataclasses import dataclass
import importlib
import math
import os
from pathlib import Path
from typing import Mapping, Optional

from flask import Flask, render_template

from stuff.tomtom import traffic_delay_seconds


REQUIRED_SETTINGS = [
    "home_pos",
    "work_pos",
    "work_miles",
    "miles_per_gallon",
    "cost_per_gallon",
    "tomtom_api_key",
]
BASE_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class MorningSettings:
    home_pos: str
    work_pos: str
    work_miles: float
    miles_per_gallon: float
    cost_per_gallon: float
    tomtom_api_key: str
    news: str = ""
    debug: bool = False

    @property
    def cost_per_day(self) -> float:
        work_miles = _finite_positive(self.work_miles, "work_miles")
        miles_per_gallon = _finite_positive(self.miles_per_gallon, "miles_per_gallon")
        cost_per_gallon = _finite_positive(self.cost_per_gallon, "cost_per_gallon")
        return round(work_miles * 2 / miles_per_gallon * cost_per_gallon, 3)


def create_app(
    settings: Optional[MorningSettings] = None,
    traffic_client=traffic_delay_seconds,
) -> Flask:
    app = Flask(
        __name__,
        static_folder=str(BASE_DIR / "static"),
        template_folder=str(BASE_DIR / "templates"),
    )
    config = settings or load_settings()

    @app.route("/")
    def work():
        return render_template(
            "index.html",
            data=str(traffic_client("work", config)),
            transport=config.cost_per_day,
            news=config.news,
        )

    @app.route("/home")
    def home():
        return render_template(
            "index.html",
            data=str(traffic_client("home", config)),
            transport=config.cost_per_day,
            news=config.news,
        )

    return app


def load_settings(env: Mapping[str, str] = os.environ, settings_module: Optional[object] = None) -> MorningSettings:
    module = settings_module if settings_module is not None else _load_optional_settings_module()
    values = {
        "home_pos": _first_value(env.get("MORNING_HOME_POS"), _module_value(module, "home_pos")),
        "work_pos": _first_value(env.get("MORNING_WORK_POS"), _module_value(module, "work_pos")),
        "work_miles": _first_value(env.get("MORNING_WORK_MILES"), _module_value(module, "work_miles")),
        "miles_per_gallon": _first_value(env.get("MORNING_MILES_PER_GALLON"), _module_value(module, "miles_per_gallon")),
        "cost_per_gallon": _first_value(env.get("MORNING_COST_PER_GALLON"), _module_value(module, "cost_per_gallon")),
        "tomtom_api_key": _first_value(env.get("TOMTOM_API_KEY"), _module_value(module, "tomtom_api_key")),
        "news": _first_value(env.get("MORNING_NEWS"), _module_value(module, "news")),
    }

    missing = [name for name in REQUIRED_SETTINGS if not values[name]]
    if missing:
        raise ValueError("missing required settings: " + ", ".join(missing))

    return MorningSettings(
        home_pos=_coordinate_pair(values["home_pos"], "home_pos"),
        work_pos=_coordinate_pair(values["work_pos"], "work_pos"),
        work_miles=_positive_float(values["work_miles"], "work_miles"),
        miles_per_gallon=_positive_float(values["miles_per_gallon"], "miles_per_gallon"),
        cost_per_gallon=_positive_float(values["cost_per_gallon"], "cost_per_gallon"),
        tomtom_api_key=_configured_api_key(values["tomtom_api_key"], "tomtom_api_key"),
        news=values["news"],
        debug=_truthy(env.get("FLASK_DEBUG", _module_value(module, "debug") or "")),
    )


def _load_optional_settings_module():
    try:
        return importlib.import_module("settings")
    except ModuleNotFoundError as error:
        if error.name != "settings":
            raise
        return None


def _module_value(settings_module: Optional[object], name: str) -> Optional[str]:
    if settings_module is None:
        return None
    value = getattr(settings_module, name, None)
    if value is None:
        return None
    return str(value)


def _first_value(*values: Optional[str]) -> str:
    for value in values:
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def _to_float(value: str, name: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"{name} must be numeric") from None


def _positive_float(value: str, name: str) -> float:
    return _finite_positive(_to_float(value, name), name)


def _finite_positive(number: float, name: str) -> float:
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return number


def _coordinate_pair(value: str, name: str) -> str:
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(f"{name} must be a numeric coordinate pair")
    normalized_parts = [part.strip() for part in parts]
    try:
        latitude = float(normalized_parts[0])
        longitude = float(normalized_parts[1])
    except ValueError:
        raise ValueError(f"{name} must be a numeric coordinate pair") from None
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        raise ValueError(f"{name} must be a numeric coordinate pair")
    return ",".join(normalized_parts)


def _configured_api_key(value: str, name: str) -> str:
    normalized = value.upper()
    if "$(" in value or normalized == "YOUR_TOMTOM_API_KEY" or normalized.startswith("REPLACE_"):
        raise ValueError(f"{name} must be configured")
    return value


def _truthy(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "t", "yes", "y", "on"}


if __name__ == "__main__":
    settings = load_settings()
    create_app(settings).run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")),
        debug=settings.debug,
    )
