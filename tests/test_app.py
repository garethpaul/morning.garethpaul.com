from types import SimpleNamespace
import unittest

from app import MorningSettings, create_app, load_settings


class AppTests(unittest.TestCase):
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

    def test_create_app_renders_work_and_home_routes_without_live_tomtom(self):
        settings = MorningSettings(
            home_pos="1,2",
            work_pos="3,4",
            work_miles=10,
            miles_per_gallon=20,
            cost_per_gallon=4,
            tomtom_api_key="key",
            news="",
        )
        calls = []

        app = create_app(settings, traffic_client=lambda where, config: calls.append((where, config)) or 123)

        with app.test_client() as client:
            work = client.get("/")
            home = client.get("/home")

        self.assertEqual(work.status_code, 200)
        self.assertEqual(home.status_code, 200)
        self.assertIn(b"123", work.data)
        self.assertEqual([call[0] for call in calls], ["work", "home"])


if __name__ == "__main__":
    unittest.main()
