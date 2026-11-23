import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import tracker


class TrackerTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "projects.json"

    def test_create_saves_project(self):
        tracker.create_project("Website", "Acme", "2026-12-31", "Sam", self.path)

        saved = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(
            saved,
            [
                {
                    "title": "Website",
                    "client": "Acme",
                    "expected_due_date": "2026-12-31",
                    "owner": "Sam",
                }
            ],
        )

    def test_list_prints_project(self):
        tracker.create_project("Website", "Acme", "2026-12-31", "Sam", self.path)

        output = io.StringIO()
        with redirect_stdout(output):
            tracker.list_projects(self.path)

        for value in ("Website", "Acme", "2026-12-31", "Sam"):
            self.assertIn(value, output.getvalue())


if __name__ == "__main__":
    unittest.main()
