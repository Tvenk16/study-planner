"""Study Planner: a command line tool that builds a study schedule for upcoming exams."""

import argparse
import sys

from datetime import date, datetime

from tabulate import tabulate

from scheduler import build_sessions, spread_topics

from storage import load_exams, save_exams


def parse_date(text):
    """Turn a YYYY-MM-DD string into a date, or stop with a clear error."""
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        sys.exit(f"Error: '{text}' is not a valid date. Use YYYY-MM-DD, like 2026-12-08.")


def parse_topic(text):
    """Turn "Classes:3" into a topic dict. A topic with no ":number" gets difficulty 1."""
    name, _, difficulty_text = text.partition(":")
    name = name.strip()
    if not difficulty_text:
        return {"name": name, "done": False, "difficulty": 1}

    if difficulty_text.strip() not in ("1", "2", "3"):
        sys.exit(f"Error: difficulty for '{name}' must be 1, 2, or 3.")
    return {"name": name, "done": False, "difficulty": int(difficulty_text)}


def find_exam(exams, name):
    """Return the exam with this name, or None. Matching ignores capitalization."""
    for exam in exams:
        if exam["name"].lower() == name.lower():
            return exam
    return None


def upcoming_exams(exams):
    """Return exams that haven't happened yet, soonest first."""
    today = date.today()
    future = [exam for exam in exams if date.fromisoformat(exam["date"]) >= today]
    return sorted(future, key=lambda exam: exam["date"])


def add_exam(args):
    exams = load_exams()
    exam_date = parse_date(args.date)

    if exam_date < date.today():
        sys.exit("Error: that date has already passed.")
    if find_exam(exams, args.name):
        sys.exit(f"Error: an exam named '{args.name}' already exists.")

    topics = [parse_topic(text) for text in args.topics.split(",") if text.strip()]
    if not topics:
        sys.exit("Error: give at least one topic, separated by commas.")

    exams.append({
        "name": args.name,
        "date": exam_date.isoformat(),
        "topics": topics,
    })
    save_exams(exams)
    print(f"Added '{args.name}' on {exam_date} with {len(topics)} topics.")


def show_countdown(args):
    exams = upcoming_exams(load_exams())
    if not exams:
        print('No upcoming exams. Add one with: python3 src/planner.py add "Name" YYYY-MM-DD "Topic1,Topic2"')
        return

    today = date.today()
    rows = []
    for exam in exams:
        days_left = (date.fromisoformat(exam["date"]) - today).days
        topics_left = sum(1 for topic in exam["topics"] if not topic["done"])
        rows.append([exam["name"], exam["date"], days_left, topics_left])
    print(tabulate(rows, headers=["Exam", "Date", "Days Left", "Topics Left"]))


def show_plan(args):
    today = date.today()
    rows = []
    for exam in upcoming_exams(load_exams()):
        remaining = [topic for topic in exam["topics"] if not topic["done"]]
        sessions = build_sessions(remaining)
        exam_date = date.fromisoformat(exam["date"])
        for study_day, topic in spread_topics(sessions, today, exam_date):
            rows.append([study_day.isoformat(), exam["name"], topic])

    if not rows:
        print("Nothing left to study. Add an exam or enjoy the break!")
        return

    # Sort by date so topics from different exams are mixed into one day-by-day list.
    rows.sort(key=lambda row: row[0])
    print(tabulate(rows, headers=["Date", "Exam", "Topic"]))


def mark_done(args):
    exams = load_exams()
    exam = find_exam(exams, args.exam)
    if exam is None:
        sys.exit(f"Error: no exam named '{args.exam}'. Run countdown to see your exams.")

    for topic in exam["topics"]:
        if topic["name"].lower() == args.topic.lower():
            if topic["done"]:
                print(f"'{topic['name']}' was already marked as done.")
                return
            topic["done"] = True
            save_exams(exams)
            print(f"Marked '{topic['name']}' as done for {exam['name']}.")
            return

    sys.exit(f"Error: '{exam['name']}' has no topic named '{args.topic}'.")


def build_parser():
    parser = argparse.ArgumentParser(description="Plan your studying before exams.")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="add an exam")
    add.add_argument("name", help='exam name, like "CS 180 Midterm"')
    add.add_argument("date", help="exam date as YYYY-MM-DD")
    add.add_argument("topics", help='comma-separated topics, optionally with difficulty 1-3, like "Classes:3,Interfaces"')
    add.set_defaults(func=add_exam)

    countdown = commands.add_parser("countdown", help="show days left for each exam")
    countdown.set_defaults(func=show_countdown)

    plan = commands.add_parser("plan", help="show a day-by-day study schedule")
    plan.set_defaults(func=show_plan)

    done = commands.add_parser("done", help="mark a topic as studied")
    done.add_argument("exam", help="exam name")
    done.add_argument("topic", help="topic name")
    done.set_defaults(func=mark_done)

    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

