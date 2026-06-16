from dataclasses import replace
import math
from types import SimpleNamespace
import os
import tempfile
import unittest

from app import MorningSettings, create_app, load_settings


class AppTests(unittest.TestCase):
    def settings(self):
        return MorningSettings(
            home_pos="1,2",
            work_pos="3,4",
            work_miles=10,
            miles_per_gallon=20,
            cost_per_gallon=4,
            tomtom_api_key="key",
            news="",
        )

    def test_load_settings_prefers_environment(self):
        settings = load_settings(
            {
                "MORNING_HOME_POS": "1,2",
                "MORNING_WORK_POS": "3,4",
                "MORNING_WORK_MILES": "12",
                "MORNING_MILES_PER_GALLON": "24",
                "MORNING_COST_PER_GALLON": "5",
                "TOMTOM_API_KEY": "key",
                "MORNING_NEWS": "Headlines",
                "FLASK_DEBUG": "false",
            }
        )

        self.assertEqual(settings.home_pos, "1,2")
        self.assertEqual(settings.work_pos, "3,4")
        self.assertEqual(settings.cost_per_day, 5.0)
        self.assertEqual(settings.news, "Headlines")
        self.assertFalse(settings.debug)

    def test_load_settings_uses_local_module_fallback(self):
        module = SimpleNamespace(
            home_pos="1,2",
            work_pos="3,4",
            work_miles="10",
            miles_per_gallon="20",
            cost_per_gallon="4",
            tomtom_api_key="key",
            news="",
            debug=False,
        )

        settings = load_settings({}, settings_module=module)

        self.assertEqual(settings.cost_per_day, 4.0)

    def test_load_settings_rejects_non_positive_numeric_settings(self):
        base_env = {
            "MORNING_HOME_POS": "1,2",
            "MORNING_WORK_POS": "3,4",
            "MORNING_WORK_MILES": "12",
            "MORNING_MILES_PER_GALLON": "24",
            "MORNING_COST_PER_GALLON": "5",
            "TOMTOM_API_KEY": "key",
        }

        cases = [
            ("MORNING_WORK_MILES", "0", "work_miles"),
            ("MORNING_MILES_PER_GALLON", "-1", "miles_per_gallon"),
            ("MORNING_COST_PER_GALLON", "0", "cost_per_gallon"),
        ]
        for key, value, setting_name in cases:
            with self.subTest(key=key):
                env = dict(base_env)
                env[key] = value
                with self.assertRaisesRegex(ValueError, f"{setting_name} must be greater than zero"):
                    load_settings(env)

    def test_load_settings_rejects_non_finite_numeric_settings(self):
        base_env = {
            "MORNING_HOME_POS": "1,2",
            "MORNING_WORK_POS": "3,4",
            "MORNING_WORK_MILES": "12",
            "MORNING_MILES_PER_GALLON": "24",
            "MORNING_COST_PER_GALLON": "5",
            "TOMTOM_API_KEY": "key",
        }
        cases = [
            ("MORNING_WORK_MILES", "nan", "work_miles"),
            ("MORNING_WORK_MILES", "inf", "work_miles"),
            ("MORNING_WORK_MILES", "-inf", "work_miles"),
            ("MORNING_MILES_PER_GALLON", "nan", "miles_per_gallon"),
            ("MORNING_MILES_PER_GALLON", "inf", "miles_per_gallon"),
            ("MORNING_MILES_PER_GALLON", "-inf", "miles_per_gallon"),
            ("MORNING_COST_PER_GALLON", "nan", "cost_per_gallon"),
            ("MORNING_COST_PER_GALLON", "inf", "cost_per_gallon"),
            ("MORNING_COST_PER_GALLON", "-inf", "cost_per_gallon"),
        ]

        for key, value, setting_name in cases:
            with self.subTest(key=key, value=value):
                env = dict(base_env)
                env[key] = value
                with self.assertRaisesRegex(ValueError, f"{setting_name} must be greater than zero"):
                    load_settings(env)

    def test_cost_per_day_rejects_non_finite_direct_values(self):
        for field in ("work_miles", "miles_per_gallon", "cost_per_gallon"):
            for value in (math.nan, math.inf, -math.inf):
                with self.subTest(field=field, value=value):
                    settings = replace(self.settings(), **{field: value})
                    with self.assertRaisesRegex(ValueError, f"{field} must be greater than zero"):
                        settings.cost_per_day

    def test_load_settings_rejects_non_numeric_settings_without_raw_cause(self):
        env = {
            "MORNING_HOME_POS": "1,2",
            "MORNING_WORK_POS": "3,4",
            "MORNING_WORK_MILES": "not-a-number",
            "MORNING_MILES_PER_GALLON": "24",
            "MORNING_COST_PER_GALLON": "5",
            "TOMTOM_API_KEY": "key",
        }

        try:
            load_settings(env)
        except ValueError as error:
            self.assertEqual(str(error), "work_miles must be numeric")
            self.assertIsNone(error.__cause__)
            self.assertNotIn("not-a-number", str(error))
        else:
            self.fail("expected non-numeric setting error")

    def test_load_settings_rejects_invalid_coordinates_without_raw_value(self):
        env = {
            "MORNING_HOME_POS": "private-home",
            "MORNING_WORK_POS": "3,4",
            "MORNING_WORK_MILES": "12",
            "MORNING_MILES_PER_GALLON": "24",
            "MORNING_COST_PER_GALLON": "5",
            "TOMTOM_API_KEY": "key",
        }

        try:
            load_settings(env)
        except ValueError as error:
            self.assertEqual(str(error), "home_pos must be a numeric coordinate pair")
            self.assertIsNone(error.__cause__)
            self.assertNotIn("private-home", str(error))
        else:
            self.fail("expected invalid coordinate setting error")

    def test_load_settings_rejects_out_of_range_coordinates_without_raw_value(self):
        base_env = {
            "MORNING_HOME_POS": "1,2",
            "MORNING_WORK_POS": "3,4",
            "MORNING_WORK_MILES": "12",
            "MORNING_MILES_PER_GALLON": "24",
            "MORNING_COST_PER_GALLON": "5",
            "TOMTOM_API_KEY": "key",
        }

        cases = [
            ("MORNING_HOME_POS", "91,2", "home_pos"),
            ("MORNING_WORK_POS", "3,181", "work_pos"),
        ]
        for key, value, setting_name in cases:
            with self.subTest(key=key):
                env = dict(base_env)
                env[key] = value
                try:
                    load_settings(env)
                except ValueError as error:
                    self.assertEqual(str(error), f"{setting_name} must be a numeric coordinate pair")
                    self.assertNotIn(value, str(error))
                else:
                    self.fail("expected out-of-range coordinate setting error")

    def test_load_settings_rejects_placeholder_tomtom_api_key(self):
        env = {
            "MORNING_HOME_POS": "1,2",
            "MORNING_WORK_POS": "3,4",
            "MORNING_WORK_MILES": "12",
            "MORNING_MILES_PER_GALLON": "24",
            "MORNING_COST_PER_GALLON": "5",
            "TOMTOM_API_KEY": "YOUR_TOMTOM_API_KEY",
        }

        try:
            load_settings(env)
        except ValueError as error:
            self.assertEqual(str(error), "tomtom_api_key must be configured")
            self.assertNotIn("YOUR_TOMTOM_API_KEY", str(error))
        else:
            self.fail("expected placeholder TomTom API key error")

    def test_create_app_renders_work_and_home_routes_without_live_tomtom(self):
        settings = self.settings()
        calls = []

        app = create_app(settings, traffic_client=lambda where, config: calls.append((where, config)) or 123)

        with app.test_client() as client:
            work = client.get("/")
            home = client.get("/home")

        self.assertEqual(work.status_code, 200)
        self.assertEqual(home.status_code, 200)
        self.assertIn(b"123", work.data)
        self.assertEqual([call[0] for call in calls], ["work", "home"])

    def test_create_app_serves_static_assets_when_cwd_changes(self):
        current_directory = os.getcwd()
        try:
            with tempfile.TemporaryDirectory() as temp_directory:
                os.chdir(temp_directory)
                app = create_app(self.settings(), traffic_client=lambda where, config: 0)
                with app.test_client() as client:
                    response = client.get("/static/styles.css")
                    status_code = response.status_code
                    body = response.get_data()
                    response.close()
        finally:
            os.chdir(current_directory)

        self.assertEqual(status_code, 200)
        self.assertIn(b".container", body)


if __name__ == "__main__":
    unittest.main()
