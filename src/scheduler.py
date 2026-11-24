"""Logic for spreading study topics across the days before an exam."""

from datetime import timedelta


def spread_topics(topics, start_date, exam_date):
    """Assign each topic a study day between start_date and the day before exam_date.

    Returns a list of (date, topic) pairs in order.
    """
    if not topics:
        return []

    # If the exam is today, there are no "days before" left, so every topic goes on
    # today as a last-minute review instead of disappearing from the plan.
    days_available = max((exam_date - start_date).days, 1)

    schedule = []
    for index, topic in enumerate(topics):
        # Scale each topic's position onto the range of available days. Integer division
        # spaces topics out evenly, and when there are more topics than days, several
        # topics share a day instead of spilling past the exam.
        day_offset = index * days_available // len(topics)
        schedule.append((start_date + timedelta(days=day_offset), topic))
    return schedule


