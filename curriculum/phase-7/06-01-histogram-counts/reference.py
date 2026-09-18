# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def histogram(values: list[float], bins: int) -> tuple[list[int], list[float]]:
    if not values or bins < 1:
        raise ValueError("need at least one value and one bin")
    lo, hi = float(min(values)), float(max(values))
    if lo == hi:
        lo, hi = lo - 0.5, hi + 0.5
    edges = [lo + i * (hi - lo) / bins for i in range(bins + 1)]
    edges[-1] = hi
    counts = [0] * bins
    for v in values:
        i = int((v - lo) / (hi - lo) * bins)
        i = min(i, bins - 1)
        # float noise: nudge onto the same side of the edge NumPy uses
        if i < bins - 1 and v >= edges[i + 1]:
            i += 1
        elif i > 0 and v < edges[i]:
            i -= 1
        counts[i] += 1
    return counts, edges
