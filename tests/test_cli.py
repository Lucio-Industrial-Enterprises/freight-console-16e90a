import subprocess
import sys
import unittest


class CliTests(unittest.TestCase):
    def test_quotes(self):
        for zone, standard in [("local", 8), ("regional", 11)]:
            for options, surcharge in [
                ([], 0),
                (["--service", "standard"], 0),
                (["--service", "express"], 7),
            ]:
                with self.subTest(zone=zone, options=options):
                    result = subprocess.run(
                        [sys.executable, "-m", "warehouse.cli", "2", zone, *options],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    self.assertEqual(result.stdout, f"${standard + surcharge:.2f}\n")
                    self.assertEqual(result.stderr, "")

    def test_invalid_service(self):
        result = subprocess.run(
            [sys.executable, "-m", "warehouse.cli", "2", "local", "--service", "overnight"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid choice", result.stderr)
        self.assertIn("overnight", result.stderr)
        self.assertEqual(result.stdout, "")
