# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import pandas as pd


class Imputer:
    def __init__(self) -> None:
        self.medians: pd.Series | None = None

    def fit(self, train: pd.DataFrame) -> "Imputer":
        self.medians = train.select_dtypes("number").median()
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.medians is None:
            raise RuntimeError("call fit before transform")
        out = df.copy()
        indicators = {}
        for col, med in self.medians.items():
            if col not in out.columns:
                continue
            indicators[f"{col}_missing"] = out[col].isna()
            out[col] = out[col].fillna(med)
        for name, flag in indicators.items():
            out[name] = flag.astype(bool)
        return out


def iqr_outlier_mask(df: pd.DataFrame, k: float = 1.5) -> pd.DataFrame:
    q1, q3 = df.quantile(0.25), df.quantile(0.75)
    iqr = q3 - q1
    return (df < q1 - k * iqr) | (df > q3 + k * iqr)
