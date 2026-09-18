# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import pandas as pd


def describe_column(s: pd.Series) -> pd.Series:
    present = s.dropna()
    if present.empty:
        raise ValueError("every value is missing")
    return pd.Series(
        {
            "count": float(present.size),
            "missing": float(s.isna().sum()),
            "mean": present.mean(),
            "median": present.median(),
            "std": present.std(ddof=1),
            "skewness": present.skew(),
            "min": present.min(),
            "max": present.max(),
        },
        dtype=float,
    )
