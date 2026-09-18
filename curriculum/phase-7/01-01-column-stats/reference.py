# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import numpy as np


def column_stats(x: np.ndarray) -> dict[str, np.ndarray]:
    return {
        "mean": x.mean(axis=0),
        "std": x.std(axis=0),
        "min": x.min(axis=0),
        "max": x.max(axis=0),
    }
