# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def _percentile(sorted_vals: list[float], p: float) -> float:
    pos = p * (len(sorted_vals) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(sorted_vals) - 1)
    frac = pos - lo
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * frac


def boxplot_summary(values: list[float]) -> dict[str, object]:
    if not values:
        raise ValueError("empty sample")
    s = sorted(float(v) for v in values)
    q1, med, q3 = _percentile(s, 0.25), _percentile(s, 0.5), _percentile(s, 0.75)
    iqr = q3 - q1
    lo_fence, hi_fence = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    whisker_low = min(v for v in s if v >= lo_fence)
    whisker_high = max(v for v in s if v <= hi_fence)
    outliers = [v for v in values if v < whisker_low or v > whisker_high]
    return {
        "q1": q1,
        "median": med,
        "q3": q3,
        "iqr": iqr,
        "whisker_low": whisker_low,
        "whisker_high": whisker_high,
        "outliers": outliers,
    }
