import pandas as pd


def describe_column(s: pd.Series) -> pd.Series:
    """count, missing, mean, median, std, skewness, min, max over the non-missing values; ValueError if all missing."""
    raise NotImplementedError
