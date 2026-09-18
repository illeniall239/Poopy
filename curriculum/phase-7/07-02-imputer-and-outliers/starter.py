import pandas as pd


class Imputer:
    """Fills NaN in numeric columns with train medians and appends <col>_missing indicator columns."""

    def fit(self, train: pd.DataFrame) -> "Imputer":
        """Record the median of every numeric column of train; return self."""
        raise NotImplementedError

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """New DataFrame with NaN filled by the fitted medians plus <col>_missing bool columns; RuntimeError if unfitted."""
        raise NotImplementedError


def iqr_outlier_mask(df: pd.DataFrame, k: float = 1.5) -> pd.DataFrame:
    """Boolean DataFrame: True where a value is outside [Q1 - k*IQR, Q3 + k*IQR] of its column; NaN is False."""
    raise NotImplementedError
