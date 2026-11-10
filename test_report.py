import tempfile
import unittest
from pathlib import Path
from report import ROOT, render, summarize


class SurveyTest(unittest.TestCase):
    def test_rates_changes_and_small_groups(self):
        rows = summarize(ROOT / "example/responses.csv")
        self.assertEqual(rows, [
            ("Harbor", "Schedule clarity", 8, 75.0, 25.0),
            ("Harbor", "Tool availability", 8, 62.5, -12.5),
            ("Juniper", "Schedule clarity", 6, 66.7, None),
        ])
        self.assertEqual(render(rows, 5), (ROOT / "example/results.md").read_text())

    def test_invalid_input_fails_before_reporting(self):
        original = (ROOT / "example/responses.csv").read_text().splitlines()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.csv"
            for invalid in (original[1], "Baseline,Harbor,Schedule clarity,extra,6", "Baseline,Harbor,,extra,4"):
                with self.subTest(invalid=invalid):
                    path.write_text("\n".join(original + [invalid]))
                    with self.assertRaises(ValueError):
                        summarize(path)
