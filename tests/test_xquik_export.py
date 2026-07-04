import json
import tempfile
import unittest
from pathlib import Path

from xquik_export import load_xquik_rows


class XquikExportTest(unittest.TestCase):
    def test_loads_nested_json_results(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            export_path = Path(temp_dir) / "xquik.json"
            export_path.write_text(
                json.dumps({"data": [{"full_text": "Useful post", "username": "demo", "like_count": 3}]}),
                encoding="utf-8",
            )

            rows = load_xquik_rows(export_path)

        self.assertEqual(rows, [{"text": "Useful post", "user": "demo", "favorite_count": 3}])

    def test_loads_jsonl_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            export_path = Path(temp_dir) / "xquik.jsonl"
            export_path.write_text('{"text":"First"}\n{"tweet":"Second","retweet_count":4}\n', encoding="utf-8")

            rows = load_xquik_rows(export_path)

        self.assertEqual(rows, [{"text": "First"}, {"text": "Second", "retweet_count": 4}])

    def test_rejects_exports_without_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            export_path = Path(temp_dir) / "xquik.json"
            export_path.write_text(json.dumps({"data": [{"id": "1"}]}), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "rows with text"):
                load_xquik_rows(export_path)


if __name__ == "__main__":
    unittest.main()
