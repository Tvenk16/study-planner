import sys
import unittest
from datetime import date
from pathlib import Path

# The tests live in tests/ but the code lives in src/, so add src/ to the import path.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from scheduler import spread_topics  # noqa: E402


class SpreadTopicsTest(unittest.TestCase):
    def test_topics_spread_evenly(self):
        schedule = spread_topics(["A", "B", "C"], date(2026, 12, 1), date(2026, 12, 7))
        days = [day for day, _ in schedule]
        self.assertEqual(days, [date(2026, 12, 1), date(2026, 12, 3), date(2026, 12, 5)])

    def test_more_topics_than_days_share_days(self):
        schedule = spread_topics(["A", "B", "C", "D"], date(2026, 12, 1), date(2026, 12, 3))
        days = [day for day, _ in schedule]
        self.assertEqual(len(schedule), 4)
        self.assertTrue(all(day < date(2026, 12, 3) for day in days))

    def test_exam_today_puts_everything_today(self):
        today = date(2026, 12, 1)
        schedule = spread_topics(["A", "B"], today, today)
        self.assertEqual([day for day, _ in schedule], [today, today])

    def test_no_topics_gives_empty_schedule(self):
        self.assertEqual(spread_topics([], date(2026, 12, 1), date(2026, 12, 7)), [])


if __name__ == "__main__":
    unittest.main()