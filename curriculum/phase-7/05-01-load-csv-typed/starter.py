import pandas as pd


def load_typed_csv(text: str, date_columns: list[str]) -> pd.DataFrame:
    """Read CSV text with pd.read_csv, then fix missing markers, money/thousands numbers and date columns."""
    raise NotImplementedError
