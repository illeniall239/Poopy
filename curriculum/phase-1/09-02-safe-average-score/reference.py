# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:
    name: str
    score: Optional[float] = None


def average_score(students: list[Student]) -> Optional[float]:
    total = 0.0
    count = 0
    for student in students:
        if student.score is not None:
            total += student.score
            count += 1
    return None if count == 0 else total / count
