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




def build_sessions(topics):
    """Turn topics into a list of study sessions, where harder topics appear more times.

    Each topic is a dict with "name" and an optional "difficulty" from 1 to 3.
    """
    # Topics saved before difficulty existed have no "difficulty" key. Treating them as 1
    # gives them one session each, so old exams plan exactly the way they did before.
    difficulties = {topic["name"]: topic.get("difficulty", 1) for topic in topics}

    # Build the list in rounds instead of repeating a hard topic back-to-back.
    # Round 1 covers every topic once, round 2 repeats topics with difficulty 2+, and
    # round 3 repeats only difficulty-3 topics. Because later rounds land later in the
    # schedule, hard topics get a second look closer to exam day.
    sessions = []
    for round_number in range(1, 4):
        for topic in topics:
            if difficulties[topic["name"]] >= round_number:
                sessions.append(topic["name"])
    return sessions


