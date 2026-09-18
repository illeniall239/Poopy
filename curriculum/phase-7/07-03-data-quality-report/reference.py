# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import pandas as pd


def quality_report(train: pd.DataFrame, test: pd.DataFrame, k: float = 3.0) -> dict[str, object]:
    nunique, count = train.nunique(), train.count()
    num_train, num_test = train.select_dtypes("number"), test.select_dtypes("number")
    std = num_train.std(ddof=1)
    drift = (num_test.mean() - num_train.mean()).abs() > k * std
    drift = drift & (std > 0)
    return {
        "duplicate_rows": int(train.duplicated().sum()),
        "missing_rate": train.isna().mean().astype(float),
        "constant_columns": [c for c in train.columns if nunique[c] <= 1],
        "id_like_columns": [c for c in train.columns if count[c] >= 2 and nunique[c] == count[c]],
        "drifted_columns": [c for c in num_train.columns if bool(drift[c])],
    }
