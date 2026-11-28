import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from scheduler import build_sessions  # noqa: E402


class BuildSessionsTest(unittest.TestCase):
    def test_harder_topics_get_more_sessions(self):
        topics = [{"name": "Easy", "difficulty": 1}, {"name": "Hard", "difficulty": 3}]
        sessions = build_sessions(topics)
        self.assertEqual(sessions.count("Easy"), 1)
        self.assertEqual(sessions.count("Hard"), 3)

    def test_every_topic_appears_before_any_repeat(self):
        topics = [{"name": "A", "difficulty": 2}, {"name": "B", "difficulty": 1}]
        self.assertEqual(build_sessions(topics), ["A", "B", "A"])

    def test_old_topics_without_difficulty_get_one_session(self):
        topics = [{"name": "A"}, {"name": "B"}]
        self.assertEqual(build_sessions(topics), ["A", "B"])


if __name__ == "__main__":
    unittest.main()