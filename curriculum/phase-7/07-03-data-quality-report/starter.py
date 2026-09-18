import pandas as pd


def quality_report(train: pd.DataFrame, test: pd.DataFrame, k: float = 3.0) -> dict[str, object]:
    """duplicate_rows, missing_rate, constant_columns, id_like_columns and drifted_columns (|Δmean| > k·std)."""
    raise NotImplementedError
