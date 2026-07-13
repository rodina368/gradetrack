"""
grades_utils.py
Helper functions for computing statistics and letter grades.
"""


def average(scores):
    """Return the average of a list of numeric scores, or None if empty."""
    if not scores:
        return None
    return round(sum(scores) / len(scores), 2)


def letter_grade(score: float) -> str:
    """Convert a numeric score (0-100) into a letter grade."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def highest_score(grades):
    """grades: list of (subject, score) tuples. Returns the (subject, score) with max score."""
    if not grades:
        return None
    return max(grades, key=lambda g: g[1])


def lowest_score(grades):
    if not grades:
        return None
    return min(grades, key=lambda g: g[1])
