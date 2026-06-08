import importlib
import json
import sys
import types
import unittest


class FakeRequest(object):
    def __init__(self, url):
        self.url = url
        self.headers = {}

    def add_header(self, name, value):
        self.headers[name] = value


class FakeResponse(object):
    def read(self):
        return json.dumps({
            "route": {"summary": {"totalDelaySeconds": 42}}
        })


class TomTomTimeoutTest(unittest.TestCase):
    def setUp(self):
        self.original_settings = sys.modules.get("settings")
        self.original_urllib2 = sys.modules.get("urllib2")
        sys.modules.pop("stuff.tomtom", None)

        settings = types.ModuleType("settings")
        settings.home_pos = "1,2"
        settings.work_pos = "3,4"
        sys.modules["settings"] = settings

        self.calls = []
        urllib2 = types.ModuleType("urllib2")
        urllib2.Request = FakeRequest

        def urlopen(request, timeout=None):
            self.calls.append((request, timeout))
            return FakeResponse()

        urllib2.urlopen = urlopen
        sys.modules["urllib2"] = urllib2

    def tearDown(self):
        sys.modules.pop("stuff.tomtom", None)
        if self.original_settings is None:
            sys.modules.pop("settings", None)
        else:
            sys.modules["settings"] = self.original_settings
        if self.original_urllib2 is None:
            sys.modules.pop("urllib2", None)
        else:
            sys.modules["urllib2"] = self.original_urllib2

    def test_get_delay_passes_timeout(self):
        tomtom = importlib.import_module("stuff.tomtom")

        self.assertEqual(42, tomtom.getDelay(tomtom.work))

        _request, timeout = self.calls[0]
        self.assertEqual(tomtom.URL_TIMEOUT_SECONDS, timeout)


if __name__ == "__main__":
    unittest.main()
