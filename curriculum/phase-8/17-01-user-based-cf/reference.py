# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math


def _cosine(a: dict[str, float], b: dict[str, float]) -> float | None:
    common = a.keys() & b.keys()
    if not common:
        return None
    dot = sum(a[i] * b[i] for i in common)
    norm_a = math.sqrt(sum(a[i] ** 2 for i in common))
    norm_b = math.sqrt(sum(b[i] ** 2 for i in common))
    return dot / (norm_a * norm_b)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def predict_rating(ratings: dict[str, dict[str, float]], user: str, item: str, k: int) -> float:
    if k < 1:
        raise ValueError("k must be at least 1")
    all_ratings = [r for row in ratings.values() for r in row.values()]
    if not all_ratings:
        raise ValueError("the ratings matrix is empty")

    mine = ratings.get(user, {})
    if not mine:
        item_ratings = [row[item] for row in ratings.values() if item in row]
        return _mean(item_ratings) if item_ratings else _mean(all_ratings)

    candidates = []
    for other, row in ratings.items():
        if other == user or item not in row:
            continue
        sim = _cosine(mine, row)
        if sim is not None and sim > 0:
            candidates.append((-sim, other, row[item]))
    if not candidates:
        return _mean(list(mine.values()))

    neighbours = sorted(candidates)[:k]  # highest similarity first, then user id
    total = sum(-neg_sim for neg_sim, _, _ in neighbours)
    return sum(-neg_sim * r for neg_sim, _, r in neighbours) / total
