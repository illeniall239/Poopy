from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    score: int


def sort_by_several_keys(players: list[Player]) -> list[Player]:
    """Return a new list of the same players by score descending, then name ascending (code points), then input order."""
    raise NotImplementedError
