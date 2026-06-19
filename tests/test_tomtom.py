from types import SimpleNamespace
import json
import unittest

import requests

from stuff.tomtom import parse_delay_seconds, route_url, traffic_delay_seconds


class FakeResponse:
    def __init__(self, body, status_error=None, close_error=None):
        self.body = body.encode() if isinstance(body, str) else body
        self.status_error = status_error
        self.close_error = close_error
        self.raised = False
        self.closed = False
        self.chunk_sizes = []

    def raise_for_status(self):
        self.raised = True
        if self.status_error:
            raise self.status_error

    def iter_content(self, chunk_size):
        self.chunk_sizes.append(chunk_size)
        for offset in range(0, len(self.body), chunk_size):
            yield self.body[offset:offset + chunk_size]

    def close(self):
        self.closed = True
        if self.close_error:
            raise self.close_error


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

    def test_parse_delay_seconds_redacts_invalid_json_body(self):
        secret = "private-provider-body-token"

        with self.assertRaisesRegex(ValueError, "^TomTom response must be valid JSON$") as raised:
            parse_delay_seconds(f"<html>{secret}</html>")

        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)
        self.assertNotIn(secret, str(raised.exception))

    def test_parse_delay_seconds_redacts_invalid_utf8_body(self):
        secret = "private-provider-byte-token"
        payload = b'{"route":"' + secret.encode() + b'\xff"}'

        with self.assertRaisesRegex(ValueError, "^TomTom response must be valid JSON$") as raised:
            parse_delay_seconds(payload)

        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)
        self.assertNotIn(secret, str(raised.exception))

    def test_parse_delay_seconds_accepts_non_negative_integers(self):
        for delay in (0, 42, " 42 "):
            with self.subTest(delay=delay):
                payload = {"route": {"summary": {"totalDelaySeconds": delay}}}
                self.assertEqual(parse_delay_seconds(payload), int(delay))

    def test_parse_delay_seconds_rejects_invalid_delay_values(self):
        for delay in (True, False, -1, 1.5, "-1", "1.5", ""):
            with self.subTest(delay=delay):
                payload = {"route": {"summary": {"totalDelaySeconds": delay}}}
                with self.assertRaisesRegex(ValueError, "must be a non-negative integer"):
                    parse_delay_seconds(payload)

    def test_traffic_delay_seconds_injects_http_get(self):
        settings = SimpleNamespace(home_pos="1,2", work_pos="3,4", tomtom_api_key="key")
        calls = []

        response = FakeResponse('{"route": {"summary": {"totalDelaySeconds": 99}}}')

        def fake_get(url, headers, timeout, stream):
            calls.append((url, headers, timeout, stream))
            return response

        self.assertEqual(traffic_delay_seconds("home", settings, http_get=fake_get), 99)
        self.assertEqual(calls[0][2], 10)
        self.assertTrue(calls[0][3])
        self.assertIn("User-Agent", calls[0][1])
        self.assertTrue(response.raised)
        self.assertTrue(response.closed)

    def test_traffic_delay_seconds_rejects_oversized_response_and_closes_it(self):
        settings = SimpleNamespace(home_pos="1,2", work_pos="3,4", tomtom_api_key="key")
        response = FakeResponse(b"x" * (1024 * 1024 + 1))

        with self.assertRaisesRegex(ValueError, "TomTom response exceeds 1 MiB limit"):
            traffic_delay_seconds("work", settings, http_get=lambda *args, **kwargs: response)

        self.assertTrue(response.closed)

    def test_traffic_delay_seconds_closes_response_when_status_check_fails(self):
        secret = "private-tomtom-key"
        settings = SimpleNamespace(home_pos="1,2", work_pos="3,4", tomtom_api_key=secret)
        response = FakeResponse(
            b"",
            status_error=requests.HTTPError(f"status failed for https://routes.tomtom.com/{secret}"),
        )

        with self.assertRaisesRegex(RuntimeError, "^TomTom request failed$") as raised:
            traffic_delay_seconds("work", settings, http_get=lambda *args, **kwargs: response)

        self.assertTrue(response.closed)
        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)
        self.assertNotIn(secret, str(raised.exception))

    def test_traffic_delay_seconds_redacts_transport_error_url(self):
        secret = "private-tomtom-key"
        settings = SimpleNamespace(home_pos="1,2", work_pos="3,4", tomtom_api_key=secret)

        def fail_request(url, **kwargs):
            raise requests.Timeout(f"timed out requesting {url}")

        with self.assertRaisesRegex(RuntimeError, "^TomTom request failed$") as raised:
            traffic_delay_seconds("work", settings, http_get=fail_request)

        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)
        self.assertNotIn(secret, str(raised.exception))

    def test_traffic_delay_seconds_redacts_response_close_errors(self):
        secret = "private-tomtom-key"
        settings = SimpleNamespace(home_pos="1,2", work_pos="3,4", tomtom_api_key=secret)
        response = FakeResponse(
            '{"route": {"summary": {"totalDelaySeconds": 99}}}',
            close_error=requests.HTTPError(f"failed closing https://routes.tomtom.com/{secret}"),
        )

        with self.assertRaisesRegex(RuntimeError, "^TomTom request failed$") as raised:
            traffic_delay_seconds("work", settings, http_get=lambda *args, **kwargs: response)

        self.assertTrue(response.closed)
        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)
        self.assertNotIn(secret, str(raised.exception))


if __name__ == "__main__":
    unittest.main()
