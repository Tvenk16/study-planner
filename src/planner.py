"""Study Planner: a command line tool that builds a study schedule for upcoming exams."""

import argparse
import sys
from datetime import date, datetime

from storage import load_exams, save_exams


def parse_date(text):
    """Turn a YYYY-MM-DD string into a date, or stop with a clear error."""
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        sys.exit(f"Error: '{text}' is not a valid date. Use YYYY-MM-DD, like 2026-12-08.")


def find_exam(exams, name):
    """Return the exam with this name, or None. Matching ignores capitalization."""
    for exam in exams:
        if exam["name"].lower() == name.lower():
            return exam
    return None


def add_exam(args):
    exams = load_exams()
    exam_date = parse_date(args.date)

    if exam_date < date.today():
        sys.exit("Error: that date has already passed.")
    if find_exam(exams, args.name):
        sys.exit(f"Error: an exam named '{args.name}' already exists.")

    topic_names = [name.strip() for name in args.topics.split(",") if name.strip()]
    if not topic_names:
        sys.exit("Error: give at least one topic, separated by commas.")

    exams.append({
        "name": args.name,
        "date": exam_date.isoformat(),
        "topics": [{"name": name, "done": False} for name in topic_names],
    })
    save_exams(exams)
    print(f"Added '{args.name}' on {exam_date} with {len(topic_names)} topics.")


def build_parser():
    parser = argparse.ArgumentParser(description="Plan your studying before exams.")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="add an exam")
    add.add_argument("name", help='exam name, like "CS 180 Midterm"')
    add.add_argument("date", help="exam date as YYYY-MM-DD")
    add.add_argument("topics", help='comma-separated topics, like "Classes,Interfaces"')
    add.set_defaults(func=add_exam)

    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

