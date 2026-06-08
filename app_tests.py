import importlib
import os
import sys
import types
import unittest


class FakeFlask(object):
    def __init__(self, name):
        self.name = name
        self.routes = []
        self.static_folder = None
        self.run_args = None

    def route(self, path):
        def decorator(func):
            self.routes.append((path, func))
            return func

        return decorator

    def run(self, **kwargs):
        self.run_args = kwargs


def install_fake_dependencies():
    flask = types.ModuleType("flask")
    flask.Flask = FakeFlask
    flask.render_template = lambda template, **_kwargs: template
    sys.modules["flask"] = flask

    tomtom = types.ModuleType("stuff.tomtom")
    tomtom.traffic = lambda _where: 0
    sys.modules["stuff.tomtom"] = tomtom

    settings = types.ModuleType("settings")
    settings.work_miles = 10
    settings.miles_per_gallon = 20
    settings.cost_per_gallon = 4
    settings.news = "news"
    sys.modules["settings"] = settings


def load_app():
    sys.modules.pop("app", None)
    install_fake_dependencies()
    return importlib.import_module("app")


class AppDebugTest(unittest.TestCase):
    def setUp(self):
        self.original_debug = os.environ.get("MORNING_DEBUG")

    def tearDown(self):
        if self.original_debug is None:
            os.environ.pop("MORNING_DEBUG", None)
        else:
            os.environ["MORNING_DEBUG"] = self.original_debug
        sys.modules.pop("app", None)

    def test_debug_is_disabled_by_default(self):
        os.environ.pop("MORNING_DEBUG", None)

        app = load_app()

        self.assertFalse(app.debug_enabled())

    def test_debug_requires_explicit_truthy_env(self):
        os.environ["MORNING_DEBUG"] = "true"

        app = load_app()

        self.assertTrue(app.debug_enabled())

    def test_debug_rejects_falsey_env(self):
        os.environ["MORNING_DEBUG"] = "false"

        app = load_app()

        self.assertFalse(app.debug_enabled())


if __name__ == "__main__":
    unittest.main()
