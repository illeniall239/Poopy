# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def most_similar(word: str, table: np.ndarray, vocab: list[str], k: int) -> list[tuple[str, float]]:
    table = np.asarray(table, dtype=float)
    if len(vocab) != table.shape[0]:
        raise ValueError("vocab and table disagree on the vocabulary size")
    if word not in vocab:
        raise ValueError(f"{word!r} is not in the vocabulary")
    if k < 0:
        raise ValueError("k must be non-negative")
    q = vocab.index(word)
    unit = table / np.linalg.norm(table, axis=1, keepdims=True)
    sims = unit @ unit[q]
    order = np.argsort(-sims, kind="stable")
    return [(vocab[i], float(sims[i])) for i in order if i != q][:k]
