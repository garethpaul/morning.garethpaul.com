import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MAKEFILE = ROOT / "Makefile"
TARGETS = ("check", "lint", "static-check", "test", "build", "compile", "verify", "clean")


class MakefileRootTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory(prefix="morning make path ")
        temp_root = Path(self.tempdir.name)
        self.checkout = temp_root / "checkout [hostile] 'quote"
        self.checkout.mkdir()
        self.makefile = self.checkout / "Makefile"
        shutil.copyfile(MAKEFILE, self.makefile)
        self.external = temp_root / "external caller"
        self.external.mkdir()

    def tearDown(self):
        self.tempdir.cleanup()

    def run_make(self, *arguments, environment=None):
        env = os.environ.copy()
        if environment:
            env.update(environment)
        return subprocess.run(
            ["make", "--no-print-directory", "-n", "-f", str(self.makefile), *arguments],
            cwd=self.external,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def assert_uses_checkout(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(self.checkout), result.stdout)
        self.assertNotIn("/tmp/attacker-root", result.stdout)

    def test_all_aliases_preserve_spaced_absolute_makefile_path(self):
        for target in TARGETS:
            with self.subTest(target=target, override="none"):
                self.assert_uses_checkout(self.run_make(target))
            with self.subTest(target=target, override="command"):
                self.assert_uses_checkout(self.run_make(target, "ROOT=/tmp/attacker-root"))
            with self.subTest(target=target, override="environment"):
                self.assert_uses_checkout(
                    self.run_make(target, environment={"ROOT": "/tmp/attacker-root"})
                )

    def test_command_line_makefile_list_override_fails_closed(self):
        result = self.run_make("check", "MAKEFILE_LIST=/tmp/attacker-root/Makefile")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MAKEFILE_LIST must not be overridden", result.stderr)

    def test_environment_makefile_list_override_fails_closed(self):
        result = self.run_make(
            "-e",
            "check",
            environment={"MAKEFILE_LIST": "/tmp/attacker-root/Makefile"},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MAKEFILE_LIST must not be overridden", result.stderr)


if __name__ == "__main__":
    unittest.main()
