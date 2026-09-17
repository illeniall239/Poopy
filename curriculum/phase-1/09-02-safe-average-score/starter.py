from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:
    name: str
    score: Optional[float] = None


def average_score(students: list[Student]) -> Optional[float]:
    """Return the average of the present scores, or None if no student has one."""
    raise NotImplementedError
