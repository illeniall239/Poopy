# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math


def user_profile(item_features: dict[str, list[float]], liked: list[str]) -> list[float]:
    if not liked:
        raise ValueError("no liked items")
    unknown = [i for i in liked if i not in item_features]
    if unknown:
        raise ValueError(f"unknown items: {unknown}")
    vectors = [item_features[i] for i in liked]
    return [sum(column) / len(vectors) for column in zip(*vectors)]


def _norm(v: list[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def recommend(profile: list[float], item_features: dict[str, list[float]], n: int, exclude: set[str]) -> list[str]:
    if n < 0:
        raise ValueError("n must be non-negative")
    profile_norm = _norm(profile)
    if profile_norm == 0:
        raise ValueError("profile is all zeros")

    def cosine(v: list[float]) -> float:
        norm = _norm(v)
        return 0.0 if norm == 0 else sum(p * x for p, x in zip(profile, v)) / (profile_norm * norm)

    candidates = [item for item in item_features if item not in exclude]
    ranked = sorted(candidates, key=lambda item: (-cosine(item_features[item]), item))
    return ranked[:n]
