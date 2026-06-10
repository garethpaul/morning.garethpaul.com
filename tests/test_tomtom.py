from types import SimpleNamespace
import json
import unittest

from stuff.tomtom import parse_delay_seconds, route_url, traffic_delay_seconds


class FakeResponse:
    def __init__(self, text):
        self.text = text
        self.raised = False

    def raise_for_status(self):
        self.raised = True


class TomTomTests(unittest.TestCase):
    def test_route_url_uses_configured_key_and_https(self):
        settings = SimpleNamespace(home_pos="1,2", work_pos="3,4", tomtom_api_key="local key")

        url = route_url("work", settings)

        self.assertTrue(url.startswith("https://routes.tomtom.com/"))
        self.assertIn("1,2:3,4", url)
        self.assertIn("local%20key", url)

    def test_parse_delay_seconds_reads_route_summary(self):
        payload = {"route": {"summary": {"totalDelaySeconds": "42"}}}

        self.assertEqual(parse_delay_seconds(payload), 42)
        self.assertEqual(parse_delay_seconds(json.dumps(payload)), 42)

    def test_parse_delay_seconds_rejects_invalid_json(self):
        with self.assertRaisesRegex(ValueError, "TomTom response must be valid JSON"):
            parse_delay_seconds("<html>not route json</html>")

    def test_traffic_delay_seconds_injects_http_get(self):
        settings = SimpleNamespace(home_pos="1,2", work_pos="3,4", tomtom_api_key="key")
        calls = []

        def fake_get(url, headers, timeout):
            calls.append((url, headers, timeout))
            return FakeResponse('{"route": {"summary": {"totalDelaySeconds": 99}}}')

        self.assertEqual(traffic_delay_seconds("home", settings, http_get=fake_get), 99)
        self.assertEqual(calls[0][2], 10)
        self.assertIn("User-Agent", calls[0][1])


if __name__ == "__main__":
    unittest.main()
