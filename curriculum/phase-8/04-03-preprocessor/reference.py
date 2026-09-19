# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math
from bisect import bisect_right

import numpy as np

KINDS = {"numeric", "log", "bucket", "category"}


class Preprocessor:
    def __init__(self, spec: dict[str, dict]):
        if not spec:
            raise ValueError("spec must name at least one column")
        for column, options in spec.items():
            kind = options.get("kind")
            if kind not in KINDS:
                raise ValueError(f"{column}: unknown kind {kind!r}")
            if kind == "bucket":
                b = options.get("boundaries")
                if not b or any(x >= y for x, y in zip(b, b[1:])):
                    raise ValueError(f"{column}: boundaries must be non-empty and strictly increasing")
        self.spec = spec
        self.stats_ = None

    def _values(self, rows: list[dict], column: str) -> list:
        try:
            values = [row[column] for row in rows]
        except KeyError:
            raise ValueError(f"a row is missing column {column!r}") from None
        if self.spec[column]["kind"] == "log":
            if any(v < 0 for v in values):
                raise ValueError(f"{column}: log columns need values >= 0")
            values = [math.log1p(v) for v in values]
        return values

    def fit(self, rows: list[dict]) -> "Preprocessor":
        if not rows:
            raise ValueError("no training rows")
        stats = {}
        for column, options in self.spec.items():
            values = self._values(rows, column)
            kind = options["kind"]
            if kind in ("numeric", "log"):
                arr = np.asarray(values, dtype=float)
                std = arr.std()
                stats[column] = (arr.mean(), std if std > 0 else 1.0)
            elif kind == "category":
                stats[column] = {v: i for i, v in enumerate(sorted(set(values)))}
        self.stats_ = stats
        return self

    def transform(self, rows: list[dict]) -> np.ndarray:
        if self.stats_ is None:
            raise RuntimeError("call fit before transform")
        blocks = []
        for column, options in self.spec.items():
            values = self._values(rows, column)
            kind = options["kind"]
            if kind in ("numeric", "log"):
                mean, std = self.stats_[column]
                blocks.append(((np.asarray(values, dtype=float) - mean) / std).reshape(-1, 1))
            else:
                if kind == "bucket":
                    b = options["boundaries"]
                    width = len(b) + 1
                    hot = [bisect_right(b, v) for v in values]
                else:
                    vocab = self.stats_[column]
                    width = len(vocab) + 1
                    hot = [vocab.get(v, len(vocab)) for v in values]
                block = np.zeros((len(rows), width))
                block[np.arange(len(rows)), hot] = 1.0
                blocks.append(block)
        return np.hstack(blocks)
