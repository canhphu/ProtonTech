import os
import tempfile
import unittest

from csv_tool import compute_stats, filter_rows, read_csv, write_csv


class CsvToolTests(unittest.TestCase):
    def test_filter_rows_contains(self) -> None:
        rows = [
            {"name": "Alice", "city": "Hanoi"},
            {"name": "Bob", "city": "Da Nang"},
        ]
        filtered = filter_rows(rows, column="city", contains="noi")
        self.assertEqual(filtered, [{"name": "Alice", "city": "Hanoi"}])

    def test_filter_rows_numeric_range(self) -> None:
        rows = [
            {"name": "A", "score": "5"},
            {"name": "B", "score": "10"},
            {"name": "C", "score": "15"},
        ]
        filtered = filter_rows(rows, column="score", min_value=6, max_value=12)
        self.assertEqual(filtered, [{"name": "B", "score": "10"}])

    def test_compute_stats(self) -> None:
        rows = [
            {"value": "2"},
            {"value": "4"},
            {"value": "6"},
        ]
        stats = compute_stats(rows, "value")
        self.assertEqual(stats["count"], 3)
        self.assertEqual(stats["min"], 2.0)
        self.assertEqual(stats["max"], 6.0)
        self.assertAlmostEqual(stats["mean"], 4.0)

    def test_read_write_csv(self) -> None:
        rows = [
            {"name": "Alice", "age": "30"},
            {"name": "Bob", "age": "25"},
        ]
        with tempfile.NamedTemporaryFile(mode="w", newline="", delete=False) as handle:
            path = handle.name

        try:
            write_csv(path, rows, fieldnames=["name", "age"])
            loaded = read_csv(path)
            self.assertEqual(loaded, rows)
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
