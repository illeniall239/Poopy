# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    score: int


def sort_by_several_keys(players: list[Player]) -> list[Player]:
    return sorted(players, key=lambda p: (-p.score, p.name))
